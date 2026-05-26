"""Voice Clone tab: batch synthesis with a reference voice."""

import logging
import gradio as gr
from modules.voice_clone import batch_clone
from modules.voice_design import list_kept_voice_numbers, get_kept_voice_path, get_kept_voice_text, TTS_LANGUAGES
from modules.utils import list_corpus_files, load_corpus, format_duration
from modules.model_manager import ModelManager
from modules.lora_pipeline import (
    STEP_PRESETS,
    get_lora_adapter_path,
    list_loras,
    run_lora_pipeline,
)
from config import DEFAULT_TARGET_SR, TTS_LANG
from lang import t

_LORA_NONE = "—"

logger = logging.getLogger(__name__)


def _read_uploaded_text_file(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def _resolve_uploaded_path(uploaded_file) -> str | None:
    if not uploaded_file:
        return None
    if isinstance(uploaded_file, str):
        return uploaded_file
    if isinstance(uploaded_file, dict):
        return uploaded_file.get("path") or uploaded_file.get("name")
    return getattr(uploaded_file, "name", str(uploaded_file))


def build_voice_clone_tab(manager: ModelManager):
    # When Irodori is the active backend, the Qwen model dropdown / non-JA
    # languages / corpus transcript field don't apply, so lock them.
    is_irodori = manager.backend == "irodori"
    qwen_interactive = not is_irodori

    resolved_ref_path = gr.State(None)
    ref_mode = gr.State(t("vc_ref_tab_shortcut"))
    corpus_mode = gr.State(t("vc_corpus_tab_file"))
    corpus_lang_state = gr.State("ja")

    with gr.Row():
        # ── Left ──
        with gr.Column(scale=3):
            gr.Markdown(t("vc_ref_section"))
            with gr.Group():
                with gr.Tabs():
                    with gr.Tab(t("vc_ref_tab_shortcut")):
                        nums = list_kept_voice_numbers()
                        shortcut_choices = [str(n) for n in nums] if nums else []
                        _init_ref_text = get_kept_voice_text(nums[0]) if nums else ""
                        shortcut_dropdown = gr.Dropdown(
                            choices=shortcut_choices,
                            label=t("vc_shortcut_label"),
                            value=shortcut_choices[0] if shortcut_choices else None,
                            allow_custom_value=False,
                        )
                    with gr.Tab(t("vc_ref_tab_upload")):
                        upload_audio = gr.Audio(label=t("vc_upload_audio_label"), type="filepath")

                ref_text = gr.Textbox(
                    label=t("vc_ref_text_label"),
                    placeholder=t("vc_ref_text_placeholder"),
                    value=_init_ref_text,
                    lines=1,
                    interactive=qwen_interactive,
                )

            refresh_btn = gr.Button(t("vc_btn_refresh_ref"), variant="secondary")

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("vc_corpus_section"))
            with gr.Group():
                with gr.Tabs():
                    with gr.Tab(t("vc_corpus_tab_file")):
                        corpus_files = list_corpus_files("ja")
                        initial_corpus = corpus_files[0] if corpus_files else None
                        if initial_corpus:
                            _init_texts = load_corpus(initial_corpus, "ja")
                            _init_chars = sum(len(t_) for t_ in _init_texts)
                        else:
                            _init_texts, _init_chars = [], 0
                        corpus_dropdown = gr.Dropdown(
                            choices=corpus_files,
                            label=t("vc_corpus_file_label"),
                            value=initial_corpus,
                        )
                    with gr.Tab(t("vc_corpus_tab_upload")):
                        upload_file = gr.File(
                            label=t("vc_corpus_upload_label"),
                            file_types=[".txt"],
                        )

                corpus_lang_radio = gr.Radio(
                    choices=(["JA"] if is_irodori else ["JA", "EN", "ZH"]),
                    value="JA",
                    label=t("vc_corpus_lang_label"),
                    interactive=qwen_interactive,
                )

                with gr.Row():
                    corpus_count = gr.Number(
                        label=t("vc_corpus_count_label"),
                        value=0, minimum=0, step=1,
                    )
                    corpus_total_lines = gr.Textbox(
                        label=t("vc_corpus_total_lines_label"),
                        value=f"{len(_init_texts)} / {len(_init_texts)} 文" if _init_texts else "",
                        interactive=False,
                    )
                    corpus_total_chars = gr.Textbox(
                        label=t("vc_corpus_total_chars_label"),
                        value=f"{_init_chars} 文字" if _init_texts else "",
                        interactive=False,
                    )

            corpus_refresh_btn = gr.Button(t("vc_btn_corpus_refresh"), variant="secondary")

        # ── Right ──
        with gr.Column(scale=2):
            gr.Markdown(t("vc_settings_section"))
            with gr.Group():
                model_choice = gr.Dropdown(
                    choices=(["Irodori-TTS-500M-v3"] if is_irodori else ModelManager.CLONE_MODELS),
                    value=("Irodori-TTS-500M-v3" if is_irodori else "1.7B-Base"),
                    label=t("vc_model_label"),
                    interactive=qwen_interactive,
                )
                tts_lang_dropdown = gr.Dropdown(
                    choices=(["japanese"] if is_irodori else TTS_LANGUAGES),
                    value=("japanese" if is_irodori else TTS_LANG),
                    label=t("vd_tts_lang_label"),
                    interactive=qwen_interactive,
                )
                target_sr = gr.Dropdown(
                    choices=[44100, 48000, 24000, 22050], value=DEFAULT_TARGET_SR, label=t("vc_sr_label"),
                )
                if is_irodori:
                    lora_choices = [_LORA_NONE, *list_loras()]
                    lora_dropdown = gr.Dropdown(
                        choices=lora_choices, value=_LORA_NONE,
                        label=t("vc_lora_label"),
                    )
                    lora_refresh_btn = gr.Button(
                        t("vc_btn_lora_refresh"), size="sm", variant="secondary",
                    )
                else:
                    lora_dropdown = gr.State(_LORA_NONE)
                    lora_refresh_btn = None

            if is_irodori:
                gr.HTML("<div style='height: 12px'></div>")
                gr.Markdown(t("vc_autotrain_section"))
                with gr.Group():
                    autotrain_toggle = gr.Checkbox(
                        value=False, label=t("vc_autotrain_label"),
                    )
                    with gr.Row():
                        autotrain_speaker = gr.Textbox(
                            label=t("lora_speaker_label"), placeholder="honoka",
                        )
                        autotrain_steps = gr.Radio(
                            choices=[(f"{k} ({v})", k) for k, v in STEP_PRESETS.items()],
                            value="quick",
                            label=t("lora_steps_label"),
                        )
            else:
                autotrain_toggle = gr.State(False)
                autotrain_speaker = gr.State("")
                autotrain_steps = gr.State("quick")

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("vc_output_section"))
            with gr.Group():
                output_folder = gr.Textbox(label=t("vc_output_folder_label"), value="clone")
                with gr.Row():
                    wavs_folder = gr.Textbox(label=t("vc_wavs_folder_label"), value="raw")
                    esd_filename = gr.Textbox(label=t("vc_esd_filename_label"), value="Neutral")
                with gr.Row():
                    clone_btn = gr.Button(t("vc_btn_start"), variant="primary", scale=3)
                    stop_btn = gr.Button(t("vc_btn_stop"), variant="secondary", scale=1)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("vc_progress_section"))
            with gr.Group():
                progress_text = gr.Textbox(label=t("vc_progress_label"), interactive=False)
                result_text = gr.Textbox(label=t("vc_result_label"), interactive=False, lines=5)

    # ── Ref: shortcut ──
    def on_shortcut_select(num_str):
        if not num_str:
            return None, "", t("vc_ref_tab_shortcut")
        num = int(num_str)
        return get_kept_voice_path(num), get_kept_voice_text(num), t("vc_ref_tab_shortcut")

    shortcut_dropdown.change(
        fn=on_shortcut_select,
        inputs=[shortcut_dropdown],
        outputs=[resolved_ref_path, ref_text, ref_mode],
    )

    def on_refresh():
        nums = list_kept_voice_numbers()
        choices = [str(n) for n in nums]
        return gr.update(choices=choices, value=choices[0] if choices else None)

    refresh_btn.click(fn=on_refresh, outputs=[shortcut_dropdown])

    upload_audio.change(
        fn=lambda v: t("vc_ref_tab_upload") if v else t("vc_ref_tab_shortcut"),
        inputs=[upload_audio],
        outputs=[ref_mode],
    )

    # ── Corpus: language selector ──
    _LANG_CODE = {"JA": "ja", "EN": "en", "ZH": "zh"}

    def on_corpus_lang_change(lang_choice, count):
        lang = _LANG_CODE.get(lang_choice, "ja")
        files = list_corpus_files(lang)
        first = files[0] if files else None
        try:
            texts = load_corpus(first, lang) if first else []
        except Exception:
            texts = []
        total = len(texts)
        limit = int(count) if count and int(count) > 0 else 0
        used = min(limit, total) if limit > 0 else total
        used_chars = sum(len(tx) for tx in texts[:used])
        lines_str = f"{used} / {total}" if texts else ""
        chars_str = f"{used_chars}" if texts else ""
        return lang, gr.update(choices=files, value=first), lines_str, chars_str

    corpus_lang_radio.change(
        fn=on_corpus_lang_change,
        inputs=[corpus_lang_radio, corpus_count],
        outputs=[corpus_lang_state, corpus_dropdown, corpus_total_lines, corpus_total_chars],
    )

    # ── Corpus: dropdown ──
    def on_corpus_dropdown_change(corpus_file, uploaded_file, count, lang):
        try:
            texts = load_corpus(corpus_file, lang) if corpus_file else []
        except Exception as e:
            logger.exception("Failed to load corpus from dropdown: %s", corpus_file)
            return t("vc_corpus_tab_file"), t("vc_err_file_load").format(e), ""
        if not texts:
            return t("vc_corpus_tab_file"), "", ""
        total = len(texts)
        limit = int(count) if count and int(count) > 0 else 0
        used = min(limit, total) if limit > 0 else total
        used_chars = sum(len(tx) for tx in texts[:used])
        return t("vc_corpus_tab_file"), f"{used} / {total}", f"{used_chars}"

    corpus_dropdown.change(
        fn=on_corpus_dropdown_change,
        inputs=[corpus_dropdown, upload_file, corpus_count, corpus_lang_state],
        outputs=[corpus_mode, corpus_total_lines, corpus_total_chars],
    )

    # ── Corpus: upload ──
    def on_upload_change(uploaded_file, corpus_file, count, lang):
        try:
            if not uploaded_file:
                texts = load_corpus(corpus_file, lang) if corpus_file else []
                mode = t("vc_corpus_tab_file")
            else:
                filepath = _resolve_uploaded_path(uploaded_file)
                if not filepath:
                    raise ValueError(t("vc_err_upload_path"))
                texts = _read_uploaded_text_file(filepath)
                mode = t("vc_corpus_tab_upload")
        except Exception as e:
            logger.exception("Failed to load corpus upload")
            return t("vc_corpus_tab_upload"), t("vc_err_file_load").format(e), ""
        if not texts:
            return mode, "", ""
        total = len(texts)
        limit = int(count) if count and int(count) > 0 else 0
        used = min(limit, total) if limit > 0 else total
        used_chars = sum(len(tx) for tx in texts[:used])
        return mode, f"{used} / {total}", f"{used_chars}"

    upload_file.change(
        fn=on_upload_change,
        inputs=[upload_file, corpus_dropdown, corpus_count, corpus_lang_state],
        outputs=[corpus_mode, corpus_total_lines, corpus_total_chars],
    )

    # ── Corpus count / refresh ──
    def on_info_refresh(mode, corpus_file, uploaded_file, count, lang):
        try:
            if mode == t("vc_corpus_tab_upload") and uploaded_file:
                filepath = _resolve_uploaded_path(uploaded_file)
                if not filepath:
                    raise ValueError(t("vc_err_upload_path"))
                texts = _read_uploaded_text_file(filepath)
            elif corpus_file:
                texts = load_corpus(corpus_file, lang)
            else:
                return "", ""
        except Exception as e:
            logger.exception("Failed to refresh corpus info")
            return t("vc_err_file_load").format(e), ""
        total = len(texts)
        limit = int(count) if count and int(count) > 0 else 0
        used = min(limit, total) if limit > 0 else total
        used_chars = sum(len(tx) for tx in texts[:used])
        return f"{used} / {total}", f"{used_chars}"

    corpus_count.change(
        fn=on_info_refresh,
        inputs=[corpus_mode, corpus_dropdown, upload_file, corpus_count, corpus_lang_state],
        outputs=[corpus_total_lines, corpus_total_chars],
    )
    corpus_refresh_btn.click(
        fn=on_info_refresh,
        inputs=[corpus_mode, corpus_dropdown, upload_file, corpus_count, corpus_lang_state],
        outputs=[corpus_total_lines, corpus_total_chars],
    )

    if is_irodori and lora_refresh_btn is not None:
        def _refresh_loras():
            return gr.update(choices=[_LORA_NONE, *list_loras()], value=_LORA_NONE)
        lora_refresh_btn.click(fn=_refresh_loras, outputs=[lora_dropdown])

    # ── Clone ──
    def on_clone(r_mode, shortcut_num, uploaded_audio, ref_t, c_mode, corpus_file, uploaded_file, count, model, tts_lang, out_folder, wavs_name, esd_name, sr, resolved_path, corpus_lang, lora_choice, do_autotrain, autotrain_spk, autotrain_st, progress=gr.Progress()):
        if r_mode == t("vc_ref_tab_upload") and uploaded_audio:
            ref = _resolve_uploaded_path(uploaded_audio)
        elif resolved_path:
            ref = resolved_path
        elif shortcut_num:
            ref = get_kept_voice_path(int(shortcut_num))
        else:
            yield t("vc_err_no_ref"), ""
            return

        if not ref:
            yield t("vc_err_ref_not_found"), ""
            return
        if manager.backend != "irodori" and not ref_t.strip():
            yield t("vc_err_empty_ref_text"), ""
            return

        try:
            if c_mode == t("vc_corpus_tab_upload") and uploaded_file:
                filepath = _resolve_uploaded_path(uploaded_file)
                if not filepath:
                    raise ValueError(t("vc_err_upload_path"))
                texts = _read_uploaded_text_file(filepath)
            elif corpus_file:
                texts = load_corpus(corpus_file, corpus_lang)
            else:
                yield t("vc_err_no_text"), ""
                return
        except Exception as e:
            logger.exception("Failed to load clone texts")
            yield t("vc_err_text_load_fail").format(e), ""
            return

        if not texts:
            yield t("vc_err_no_text"), ""
            return

        limit = int(count) if count and int(count) > 0 else 0
        if limit > 0:
            texts = texts[:limit]

        esd = esd_name.strip() or "Neutral"
        if not esd.endswith(".txt"):
            esd += ".txt"

        lora_path: str | None = None
        if manager.backend == "irodori" and lora_choice and lora_choice != _LORA_NONE:
            lora_path = get_lora_adapter_path(lora_choice)

        clone_result_lines: list[str] = []
        clone_stats: dict | None = None
        try:
            for pct, payload in batch_clone(
                manager, ref_audio=ref, ref_text=ref_t, texts=texts,
                output_folder=out_folder.strip() or "clone",
                wavs_folder=wavs_name.strip() or "raw",
                esd_filename=esd,
                model_key=model, target_sr=int(sr),
                corpus_lang=corpus_lang,
                tts_language=tts_lang,
                lora_path=lora_path,
            ):
                if isinstance(payload, dict):
                    clone_stats = payload
                    result = t("vc_result_files").format(
                        payload["total_files"],
                        format_duration(payload["total_duration_sec"]),
                        payload["output_dir"],
                        payload["esd_path"],
                    )
                    clone_result_lines.append(result)
                    yield t("vc_ok_done"), result
                else:
                    progress(pct, desc=payload)
                    yield payload, ""
        except Exception as e:
            if "cancel" in type(e).__name__.lower() or "cancel" in str(e).lower():
                yield t("vc_stopped"), ""
            else:
                logger.exception("Clone failed")
                yield t("vc_clone_fail").format(e), ""
            return

        # ── Chain into LoRA training when the user opted in ──
        if (
            manager.backend == "irodori"
            and do_autotrain
            and clone_stats is not None
            and (autotrain_spk or "").strip()
        ):
            out_folder_name = (out_folder.strip() or "clone")
            try:
                for ev in run_lora_pipeline(
                    source=out_folder_name,
                    speaker=autotrain_spk.strip(),
                    steps=autotrain_st,
                ):
                    kind = ev.get("event")
                    if kind == "stage":
                        line = f"[{ev['status']}] {ev.get('message', '')}"
                        clone_result_lines.append(line)
                        yield line, "\n".join(clone_result_lines[-40:])
                    elif kind == "progress":
                        line = f"train step {ev.get('step')}/{ev.get('max_steps')}"
                        if ev.get("loss") is not None:
                            line += f"  loss={ev['loss']:.4f}"
                        yield line, "\n".join(clone_result_lines[-39:] + [line])
                    elif kind == "log":
                        clone_result_lines.append(ev.get("raw", ""))
                    elif kind == "done":
                        summary = t("lora_ok_done").format(
                            ev.get("speaker"), ev.get("output_dir"),
                        )
                        clone_result_lines.append(summary)
                        yield t("vc_autotrain_done"), "\n".join(clone_result_lines[-40:])
            except Exception as e:
                logger.exception("Auto-train LoRA pipeline failed")
                yield t("lora_err_failed").format(e), "\n".join(clone_result_lines[-40:])

    clone_event = clone_btn.click(
        fn=on_clone,
        inputs=[
            ref_mode, shortcut_dropdown, upload_audio, ref_text,
            corpus_mode, corpus_dropdown, upload_file, corpus_count,
            model_choice, tts_lang_dropdown, output_folder, wavs_folder, esd_filename, target_sr, resolved_ref_path,
            corpus_lang_state,
            lora_dropdown, autotrain_toggle, autotrain_speaker, autotrain_steps,
        ],
        outputs=[progress_text, result_text],
    )
    stop_btn.click(fn=None, cancels=[clone_event])
