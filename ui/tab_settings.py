"""Settings tab: backend selection, language switching, and system info."""

import os
import sys
import time
import threading
import subprocess
import gradio as gr
from modules.model_manager import ModelManager, BACKENDS, BACKEND_LABELS, _faster_available, _irodori_available
from config import LANG, save_lang, save_backend
from lang import t


def _backend_choices() -> list[tuple[str, str]]:
    """Return (label, internal_key) pairs filtered by what's actually installed."""
    pairs = []
    for key in BACKENDS:
        if key == "faster" and not _faster_available():
            continue
        if key == "irodori" and not _irodori_available():
            continue
        pairs.append((BACKEND_LABELS[key], key))
    return pairs

_LANG_CHOICES = [
    ("日本語", "ja"),
    ("English", "en"),
    ("中文", "zh"),
    ("한국어", "ko"),
]


def build_settings_tab(manager: ModelManager):
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown(t("settings_backend_section"))
            with gr.Group():
                gr.Markdown(t("settings_backend_desc"))
                backend_dropdown = gr.Dropdown(
                    choices=_backend_choices(),
                    value=manager.backend,
                    label=t("settings_backend_label"),
                    interactive=True,
                )
                backend_status = gr.Textbox(
                    value=_backend_status_text(manager),
                    label=t("settings_backend_status_label"),
                    interactive=False,
                )

        with gr.Column(scale=2):
            gr.Markdown(t("settings_sysinfo_section"))
            with gr.Group():
                gr.Textbox(
                    value=manager.get_gpu_name(),
                    label=t("settings_gpu_label"), interactive=False,
                )
                vram_info = gr.Textbox(
                    value=manager.get_vram_info(),
                    label=t("settings_vram_label"), interactive=False,
                )
                gr.Textbox(
                    value=t("settings_faster_installed") if _faster_available() else t("settings_faster_not_installed"),
                    label="faster-qwen3-tts", interactive=False,
                )
                gr.Textbox(
                    value=t("settings_irodori_installed") if _irodori_available() else t("settings_irodori_not_installed"),
                    label="Irodori-TTS", interactive=False,
                )
                refresh_btn = gr.Button(t("settings_btn_refresh"), variant="secondary")

    gr.HTML("<div style='height: 12px'></div>")

    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown(t("settings_lang_section"))
            with gr.Group():
                lang_dropdown = gr.Dropdown(
                    choices=[label for label, _ in _LANG_CHOICES],
                    value=_lang_label(LANG),
                    label=t("settings_lang_label"),
                )
                gr.Markdown(f"_{t('settings_lang_note')}_")
                lang_btn = gr.Button("Apply & Restart", variant="primary")
                lang_status = gr.Textbox(label="Status", interactive=False)

    # ── Backend ──
    def on_backend_change(backend):
        try:
            manager.set_backend(backend)
            save_backend(backend)
        except Exception as e:
            return t("settings_backend_err").format(e)

        # Backend switching changes which controls are locked in the Design /
        # Clone tabs. Auto-restart so those tabs render with the correct state.
        def _restart():
            time.sleep(1.5)
            env = os.environ.copy()
            env["VDC_RESTART"] = "1"
            subprocess.Popen([sys.executable] + sys.argv, env=env)
            os._exit(0)

        threading.Thread(target=_restart, daemon=True).start()
        return t("settings_backend_restart")

    backend_dropdown.change(
        fn=on_backend_change,
        inputs=[backend_dropdown],
        outputs=[backend_status],
        js="(b) => { setTimeout(() => { function poll(){ fetch('/').then(() => location.reload()).catch(() => setTimeout(poll, 500)); } poll(); }, 2000); return [b]; }",
    )

    def on_refresh():
        return manager.get_vram_info()

    refresh_btn.click(fn=on_refresh, outputs=[vram_info])

    # ── Language ──
    def on_apply_lang(label):
        code = _lang_code(label)
        try:
            save_lang(code)
        except Exception as e:
            return t("settings_lang_save_fail").format(e)

        def _restart():
            time.sleep(1.5)
            env = os.environ.copy()
            env["VDC_RESTART"] = "1"
            subprocess.Popen([sys.executable] + sys.argv, env=env)
            os._exit(0)

        threading.Thread(target=_restart, daemon=True).start()
        return "再起動中... / Restarting... / 重启中..."

    lang_btn.click(
        fn=on_apply_lang,
        inputs=[lang_dropdown],
        outputs=[lang_status],
        js="(label) => { setTimeout(() => { function poll(){ fetch('/').then(() => location.reload()).catch(() => setTimeout(poll, 500)); } poll(); }, 2000); return [label]; }",
    )


def _lang_label(code: str) -> str:
    for label, c in _LANG_CHOICES:
        if c == code:
            return label
    return _LANG_CHOICES[0][0]


def _lang_code(label: str) -> str:
    for lbl, code in _LANG_CHOICES:
        if lbl == label:
            return code
    return "ja"


def _backend_status_text(manager: ModelManager) -> str:
    status = t("settings_backend_current").format(manager.backend)
    if not _faster_available():
        status += t("settings_backend_no_faster")
    return status
