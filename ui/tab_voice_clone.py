"""Voice Clone tab: batch synthesis with a reference voice."""

import logging
import gradio as gr
from modules.voice_clone import batch_clone
from modules.voice_design import list_kept_voice_numbers, get_kept_voice_path, get_kept_voice_text
from modules.utils import list_corpus_files, load_corpus, format_duration
from modules.model_manager import ModelManager
from config import DEFAULT_TARGET_SR

logger = logging.getLogger(__name__)


def _read_uploaded_text_file(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def _resolve_uploaded_path(uploaded_file) -> str | None:
    """Resolve Gradio upload value into a local filepath."""
    if not uploaded_file:
        return None
    if isinstance(uploaded_file, str):
        return uploaded_file
    if isinstance(uploaded_file, dict):
        # Gradio may provide {"path": "..."} depending on version/component.
        return uploaded_file.get("path") or uploaded_file.get("name")
    return getattr(uploaded_file, "name", str(uploaded_file))


def build_voice_clone_tab(manager: ModelManager):
    resolved_ref_path = gr.State(None)
    ref_mode = gr.State("ショートカット")
    corpus_mode = gr.State("ファイル選択")

    with gr.Row():
        # ── Left ──
        with gr.Column(scale=3):
            gr.Markdown("### 1. 参照音声")
            with gr.Group():
                with gr.Tabs():
                    with gr.Tab("ショートカット"):
                        nums = list_kept_voice_numbers()
                        shortcut_choices = [str(n) for n in nums] if nums else []
                        _init_ref_text = get_kept_voice_text(nums[0]) if nums else ""
                        shortcut_dropdown = gr.Dropdown(
                            choices=shortcut_choices,
                            label="voice_design 番号",
                            value=shortcut_choices[0] if shortcut_choices else None,
                            allow_custom_value=False,
                        )
                    with gr.Tab("アップロード"):
                        upload_audio = gr.Audio(label="音声ファイル", type="filepath")

                ref_text = gr.Textbox(
                    label="参照音声の書き起こし",
                    placeholder="ショートカットなら自動入力",
                    value=_init_ref_text,
                    lines=1,
                )

            refresh_btn = gr.Button("リスト更新", variant="secondary")

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown("### 2. コーパス")
            with gr.Group():
                with gr.Tabs():
                    with gr.Tab("ファイル選択"):
                        corpus_files = list_corpus_files()
                        initial_corpus = corpus_files[0] if corpus_files else None
                        if initial_corpus:
                            _init_texts = load_corpus(initial_corpus)
                            _init_chars = sum(len(t) for t in _init_texts)
                        else:
                            _init_texts, _init_chars = [], 0
                        corpus_dropdown = gr.Dropdown(
                            choices=corpus_files,
                            label="コーパスファイル",
                            value=initial_corpus,
                        )
                    with gr.Tab("アップロード"):
                        upload_file = gr.File(
                            label="テキストファイル（1行1文の.txt）",
                            file_types=[".txt"],
                        )

                with gr.Row():
                    corpus_count = gr.Number(
                        label="使用する文数（0=すべて）",
                        value=0, minimum=0, step=1,
                    )
                    corpus_total_lines = gr.Textbox(
                        label="総文数",
                        value=f"{len(_init_texts)} / {len(_init_texts)} 文" if _init_texts else "",
                        interactive=False,
                    )
                    corpus_total_chars = gr.Textbox(
                        label="総文字数",
                        value=f"{_init_chars} 文字" if _init_texts else "",
                        interactive=False,
                    )

            corpus_refresh_btn = gr.Button("コーパス情報を更新", variant="secondary")

        # ── Right ──
        with gr.Column(scale=2):
            gr.Markdown("### 3. 設定")
            with gr.Group():
                model_choice = gr.Dropdown(
                    choices=ModelManager.CLONE_MODELS, value="1.7B-Base", label="モデル",
                )
                target_sr = gr.Dropdown(
                    choices=[44100, 48000, 24000, 22050], value=DEFAULT_TARGET_SR, label="出力サンプルレート (Hz)",
                )

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown("### 出力先（output/）")
            with gr.Group():
                output_folder = gr.Textbox(label="フォルダ名", value="clone")
                with gr.Row():
                    wavs_folder = gr.Textbox(label="音声サブフォルダ名", value="raw")
                    esd_filename = gr.Textbox(label="テキストリスト名（.txt自動付与）", value="Neutral")
                with gr.Row():
                    clone_btn = gr.Button("一括生成開始", variant="primary", scale=3)
                    stop_btn = gr.Button("■ 停止", variant="secondary", scale=1)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown("### 4. 進捗")
            with gr.Group():
                progress_text = gr.Textbox(label="ステータス", interactive=False)
                result_text = gr.Textbox(label="結果", interactive=False, lines=5)

    # ── Ref: shortcut interaction → shortcut mode ──
    def on_shortcut_select(num_str):
        if not num_str:
            return None, "", "ショートカット"
        num = int(num_str)
        return get_kept_voice_path(num), get_kept_voice_text(num), "ショートカット"

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

    # ── Ref: audio upload → upload mode ──
    upload_audio.change(
        fn=lambda v: "アップロード" if v else "ショートカット",
        inputs=[upload_audio],
        outputs=[ref_mode],
    )

    # ── Corpus: dropdown interaction → file select mode ──
    def on_corpus_dropdown_change(corpus_file, uploaded_file, count):
        try:
            texts = load_corpus(corpus_file) if corpus_file else []
        except Exception as e:
            logger.exception("Failed to load corpus from dropdown: %s", corpus_file)
            return "ファイル選択", f"エラー: {e}", ""
        if not texts:
            return "ファイル選択", "", ""
        total = len(texts)
        limit = int(count) if count and int(count) > 0 else 0
        used = min(limit, total) if limit > 0 else total
        used_chars = sum(len(t) for t in texts[:used])
        return "ファイル選択", f"{used} / {total} 文", f"{used_chars} 文字"

    corpus_dropdown.change(
        fn=on_corpus_dropdown_change,
        inputs=[corpus_dropdown, upload_file, corpus_count],
        outputs=[corpus_mode, corpus_total_lines, corpus_total_chars],
    )

    # ── Corpus: file upload → upload mode ──
    def on_upload_change(uploaded_file, corpus_file, count):
        try:
            if not uploaded_file:
                texts = load_corpus(corpus_file) if corpus_file else []
                mode = "ファイル選択"
            else:
                filepath = _resolve_uploaded_path(uploaded_file)
                if not filepath:
                    raise ValueError("アップロードされたファイルのパスを解決できませんでした")
                texts = _read_uploaded_text_file(filepath)
                mode = "アップロード"
        except Exception as e:
            logger.exception("Failed to load corpus upload")
            return "アップロード", f"エラー: {e}", ""
        if not texts:
            return mode, "", ""
        total = len(texts)
        limit = int(count) if count and int(count) > 0 else 0
        used = min(limit, total) if limit > 0 else total
        used_chars = sum(len(t) for t in texts[:used])
        return mode, f"{used} / {total} 文", f"{used_chars} 文字"

    upload_file.change(
        fn=on_upload_change,
        inputs=[upload_file, corpus_dropdown, corpus_count],
        outputs=[corpus_mode, corpus_total_lines, corpus_total_chars],
    )

    # ── Corpus count change / refresh ──
    def on_info_refresh(mode, corpus_file, uploaded_file, count):
        try:
            if mode == "アップロード" and uploaded_file:
                filepath = _resolve_uploaded_path(uploaded_file)
                if not filepath:
                    raise ValueError("アップロードされたファイルのパスを解決できませんでした")
                texts = _read_uploaded_text_file(filepath)
            elif corpus_file:
                texts = load_corpus(corpus_file)
            else:
                return "", ""
        except Exception as e:
            logger.exception("Failed to refresh corpus info")
            return f"エラー: {e}", ""
        total = len(texts)
        limit = int(count) if count and int(count) > 0 else 0
        used = min(limit, total) if limit > 0 else total
        used_chars = sum(len(t) for t in texts[:used])
        return f"{used} / {total} 文", f"{used_chars} 文字"

    corpus_count.change(
        fn=on_info_refresh,
        inputs=[corpus_mode, corpus_dropdown, upload_file, corpus_count],
        outputs=[corpus_total_lines, corpus_total_chars],
    )
    corpus_refresh_btn.click(
        fn=on_info_refresh,
        inputs=[corpus_mode, corpus_dropdown, upload_file, corpus_count],
        outputs=[corpus_total_lines, corpus_total_chars],
    )

    # ── Clone ──
    def on_clone(r_mode, shortcut_num, uploaded_audio, ref_t, c_mode, corpus_file, uploaded_file, count, model, out_folder, wavs_name, esd_name, sr, resolved_path, progress=gr.Progress()):
        if r_mode == "アップロード" and uploaded_audio:
            ref = _resolve_uploaded_path(uploaded_audio)
        elif resolved_path:
            ref = resolved_path
        elif shortcut_num:
            ref = get_kept_voice_path(int(shortcut_num))
        else:
            yield "エラー: 参照音声がありません", ""
            return

        if not ref:
            yield "エラー: 参照音声が見つかりません", ""
            return
        if not ref_t.strip():
            yield "エラー: 書き起こしテキストが空です", ""
            return

        try:
            if c_mode == "アップロード" and uploaded_file:
                filepath = _resolve_uploaded_path(uploaded_file)
                if not filepath:
                    raise ValueError("アップロードされたファイルのパスを解決できませんでした")
                texts = _read_uploaded_text_file(filepath)
            elif corpus_file:
                texts = load_corpus(corpus_file)
            else:
                yield "エラー: テキストがありません", ""
                return
        except Exception as e:
            logger.exception("Failed to load clone texts")
            yield f"エラー: テキスト読み込み失敗 ({e})", ""
            return

        if not texts:
            yield "エラー: テキストがありません", ""
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
            ):
                if isinstance(payload, dict):
                    stats = payload
                    result = (
                        f"ファイル数: {stats['total_files']}\n"
                        f"総音声時間: {format_duration(stats['total_duration_sec'])}\n"
                        f"出力先: {stats['output_dir']}\n"
                        f"テキストリスト: {stats['esd_path']}"
                    )
                    yield "完了!", result
                else:
                    progress(pct, desc=payload)
                    yield payload, ""
        except Exception as e:
            if "cancel" in type(e).__name__.lower() or "cancel" in str(e).lower():
                yield "停止しました", ""
            else:
                logger.exception("Clone failed")
                yield f"エラー: {e}", ""

    clone_event = clone_btn.click(
        fn=on_clone,
        inputs=[
            ref_mode, shortcut_dropdown, upload_audio, ref_text,
            corpus_mode, corpus_dropdown, upload_file, corpus_count,
            model_choice, output_folder, wavs_folder, esd_filename, target_sr, resolved_ref_path,
        ],
        outputs=[progress_text, result_text],
    )
    stop_btn.click(fn=None, cancels=[clone_event])
