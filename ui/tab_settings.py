"""Settings tab: backend selection and system info."""

import gradio as gr
from modules.model_manager import ModelManager, BACKENDS, _faster_available


def build_settings_tab(manager: ModelManager):
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 推論バックエンド")
            with gr.Group():
                gr.Markdown(
                    "**faster**: CUDA Graph高速化（6-10倍速、GPU専用）\n\n"
                    "**standard**: 標準推論（CPU/GPU両対応）"
                )
                backend_dropdown = gr.Dropdown(
                    choices=BACKENDS,
                    value=manager.backend,
                    label="バックエンド",
                    interactive=_faster_available(),
                )
                backend_status = gr.Textbox(
                    value=_backend_status_text(manager),
                    label="ステータス",
                    interactive=False,
                )

        with gr.Column(scale=2):
            gr.Markdown("### システム情報")
            with gr.Group():
                gr.Textbox(
                    value=manager.get_gpu_name(),
                    label="GPU", interactive=False,
                )
                vram_info = gr.Textbox(
                    value=manager.get_vram_info(),
                    label="VRAM", interactive=False,
                )
                gr.Textbox(
                    value="インストール済み" if _faster_available() else "未インストール（pip install faster-qwen3-tts）",
                    label="faster-qwen3-tts", interactive=False,
                )
                refresh_btn = gr.Button("更新", variant="secondary")

    def on_backend_change(backend):
        try:
            manager.set_backend(backend)
            return _backend_status_text(manager)
        except Exception as e:
            return f"エラー: {e}"

    backend_dropdown.change(
        fn=on_backend_change,
        inputs=[backend_dropdown],
        outputs=[backend_status],
    )

    def on_refresh():
        return manager.get_vram_info()

    refresh_btn.click(fn=on_refresh, outputs=[vram_info])


def _backend_status_text(manager: ModelManager) -> str:
    status = f"現在: {manager.backend}"
    if not _faster_available():
        status += "（faster未インストール）"
    return status
