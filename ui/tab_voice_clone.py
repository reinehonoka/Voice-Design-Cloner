"""Voice Clone tab: batch synthesis with a reference voice."""

import logging
import gradio as gr
from modules.voice_clone import batch_clone
from modules.voice_design import list_kept_voice_numbers, get_kept_voice_path, get_kept_voice_text, TTS_LANGUAGES
from modules.utils import list_corpus_files, load_corpus, format_duration
from modules.model_manager import ModelManager
from config import DEFAULT_TARGET_SR, TTS_LANG
from lang import t

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
                    choices=["JA", "EN", "ZH"],
                    value="JA",
                    label=t("vc_corpus_lang_label"),
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
                    choices=ModelManager.CLONE_MODELS, value="1.7B-Base", label=t("vc_model_label"),
                )
                tts_lang_dropdown = gr.Dropdown(
                    choices=TTS_LANGUAGES,
                    value=TTS_LANG,
                    label=t("vd_tts_lang_label"),
                )
                target_sr = gr.Dropdown(
                    choices=[44100, 48000, 24000, 22050], value=DEFAULT_TARGET_SR, label=t("vc_sr_label"),
                )

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

    # ── Clone ──
    def on_clone(r_mode, shortcut_num, uploaded_audio, ref_t, c_mode, corpus_file, uploaded_file, count, model, tts_lang, out_folder, wavs_name, esd_name, sr, resolved_path, corpus_lang, progress=gr.Progress()):
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
        if not ref_t.strip():
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

        try:
            for pct, payload in batch_clone(
                manager, ref_audio=ref, ref_text=ref_t, texts=texts,
                output_folder=out_folder.strip() or "clone",
                wavs_folder=wavs_name.strip() or "raw",
                esd_filename=esd,
                model_key=model, target_sr=int(sr),
                corpus_lang=corpus_lang,
                tts_language=tts_lang,
            ):
                if isinstance(payload, dict):
                    stats = payload
                    result = t("vc_result_files").format(
                        stats["total_files"],
                        format_duration(stats["total_duration_sec"]),
                        stats["output_dir"],
                        stats["esd_path"],
                    )
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

    clone_event = clone_btn.click(
        fn=on_clone,
        inputs=[
            ref_mode, shortcut_dropdown, upload_audio, ref_text,
            corpus_mode, corpus_dropdown, upload_file, corpus_count,
            model_choice, tts_lang_dropdown, output_folder, wavs_folder, esd_filename, target_sr, resolved_ref_path,
            corpus_lang_state,
        ],
        outputs=[progress_text, result_text],
    )
    stop_btn.click(fn=None, cancels=[clone_event])
