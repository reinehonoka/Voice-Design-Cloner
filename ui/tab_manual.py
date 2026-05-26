"""Manual tab: usage guide."""

import gradio as gr
from lang import t


def build_manual_tab():
    gr.Markdown(t("manual_intro"))
    gr.Markdown("---")
    gr.Markdown(t("manual_voice_design"))
    gr.Markdown("---")
    gr.Markdown(t("manual_voice_clone"))
    gr.Markdown("---")
    gr.Markdown(t("manual_tools"))
    gr.Markdown("---")
    gr.Markdown(t("manual_settings"))
    gr.Markdown("---")
    gr.Markdown(t("manual_irodori"))
    gr.Markdown("---")
    gr.Markdown(t("manual_sbv2"))
    gr.Markdown("---")
    gr.Markdown(t("manual_vram"))
