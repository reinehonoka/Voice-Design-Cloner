"""Irodori-TTS Inference tab: single-utterance playground for v3 + optional LoRA.

Mirrors ``master/lora/test_lora.py`` as a GUI: pick a reference voice, optionally
attach a trained LoRA, type a line, generate, preview, and save with a custom
name to ``output/irodori_infer/``. Useful for trying out a freshly-trained LoRA
before running a full corpus batch via the Voice Clone tab.
"""

import logging
import gradio as gr

from lang import t
from modules.lora_pipeline import get_lora_adapter_path, get_lora_training_wav, list_loras
from modules.model_manager import ModelManager
from modules.voice_design import (
    generate_clone_oneshot_irodori,
    get_kept_voice_path,
    get_kept_voice_text,
    list_kept_voice_numbers,
    save_irodori_infer,
)

logger = logging.getLogger(__name__)

_LORA_NONE = "—"


def build_irodori_infer_tab(manager: ModelManager):
    is_irodori = manager.backend == "irodori"

    with gr.Row():
        # ── Left: reference + LoRA + caption + text ──
        with gr.Column(scale=3):
            gr.Markdown(t("ii_ref_section"))
            with gr.Group():
                with gr.Tabs():
                    with gr.Tab(t("vc_ref_tab_shortcut")):
                        nums = list_kept_voice_numbers()
                        shortcut_choices = [str(n) for n in nums] if nums else []
                        shortcut_dropdown = gr.Dropdown(
                            choices=shortcut_choices,
                            label=t("vc_shortcut_label"),
                            value=shortcut_choices[0] if shortcut_choices else None,
                            interactive=is_irodori,
                        )
                    with gr.Tab(t("vc_ref_tab_upload")):
                        upload_audio = gr.Audio(
                            label=t("vc_upload_audio_label"), type="filepath",
                            interactive=is_irodori,
                        )
                refresh_ref_btn = gr.Button(t("vc_btn_refresh_ref"), variant="secondary", interactive=is_irodori)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("ii_model_section"))
            with gr.Group():
                lora_dropdown = gr.Dropdown(
                    choices=[_LORA_NONE, *list_loras()],
                    value=_LORA_NONE,
                    label=t("vc_lora_label"),
                    interactive=is_irodori,
                )
                lora_refresh_btn = gr.Button(t("vc_btn_lora_refresh"), variant="secondary", interactive=is_irodori)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("ii_text_section"))
            with gr.Group():
                text_input = gr.Textbox(
                    label=t("ii_text_label"),
                    placeholder=t("ii_text_placeholder"),
                    lines=4,
                    interactive=is_irodori,
                )

        # ── Right: params + preview + save ──
        with gr.Column(scale=2):
            gr.Markdown(t("ii_params_section"))
            with gr.Group():
                seed_input = gr.Number(
                    label=t("ii_seed_label"),
                    value=None, precision=0,
                    interactive=is_irodori,
                )
                seed_random_btn = gr.Button(t("ii_btn_seed_random"), size="sm", interactive=is_irodori)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("ii_preview_section"))
            with gr.Group():
                audio_preview = gr.Audio(label=t("vd_preview_label"), type="numpy")
                status = gr.Textbox(label=t("vd_status_label"), interactive=False)
                with gr.Row():
                    generate_btn = gr.Button(t("vd_btn_generate"), variant="primary", scale=2, interactive=is_irodori)
                    reroll_btn = gr.Button(t("vd_btn_reroll"), variant="secondary", scale=1, interactive=is_irodori)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("ii_save_section"))
            with gr.Group():
                save_name = gr.Textbox(label=t("vd_save_name_label"), value="irodori_infer", interactive=is_irodori)
                save_btn = gr.Button(t("vd_btn_save"), variant="primary", interactive=is_irodori)

    if not is_irodori:
        gr.Markdown(t("ii_irodori_only_note"))

    state_audio = gr.State()

    # ── Helpers ──
    def on_refresh_ref():
        nums = list_kept_voice_numbers()
        choices = [str(n) for n in nums]
        return gr.update(choices=choices, value=choices[0] if choices else None)

    refresh_ref_btn.click(fn=on_refresh_ref, outputs=[shortcut_dropdown])

    lora_refresh_btn.click(
        fn=lambda: gr.update(choices=[_LORA_NONE, *list_loras()], value=_LORA_NONE),
        outputs=[lora_dropdown],
    )

    # Auto-fill reference upload from the LoRA's training data so the user can
    # speak with just LoRA + text (no manual ref selection).
    def _on_lora_change(lora_choice):
        if not lora_choice or lora_choice == _LORA_NONE:
            return gr.update()
        wav = get_lora_training_wav(lora_choice)
        return gr.update(value=wav) if wav else gr.update()

    lora_dropdown.change(fn=_on_lora_change, inputs=[lora_dropdown], outputs=[upload_audio])

    seed_random_btn.click(fn=lambda: None, outputs=[seed_input])

    # ── Generate ──
    def on_generate(shortcut_num, uploaded_audio, lora_choice, text, seed):
        if not is_irodori:
            return None, None, t("ii_err_not_irodori")
        if not text or not text.strip():
            return None, None, t("ii_err_no_text")

        if uploaded_audio:
            ref_wav = uploaded_audio if isinstance(uploaded_audio, str) else (
                uploaded_audio.get("path") or uploaded_audio.get("name")
                if isinstance(uploaded_audio, dict) else getattr(uploaded_audio, "name", None)
            )
        elif shortcut_num:
            ref_wav = get_kept_voice_path(int(shortcut_num))
        else:
            return None, None, t("ii_err_no_ref")

        if not ref_wav:
            return None, None, t("ii_err_ref_not_found")

        lora_path = None
        if lora_choice and lora_choice != _LORA_NONE:
            lora_path = get_lora_adapter_path(lora_choice)

        try:
            sr, audio = generate_clone_oneshot_irodori(
                text=text.strip(),
                ref_wav=ref_wav,
                caption=None,
                lora_path=lora_path,
                seed=(int(seed) if seed is not None else None),
            )
            return (sr, audio), (sr, audio), t("vd_ok_generated").format(sr)
        except Exception as e:
            logger.exception("Irodori inference failed")
            return None, None, t("vd_err_generate_fail").format(e)

    gen_inputs = [shortcut_dropdown, upload_audio, lora_dropdown, text_input, seed_input]
    gen_outputs = [audio_preview, state_audio, status]
    generate_btn.click(fn=on_generate, inputs=gen_inputs, outputs=gen_outputs)
    reroll_btn.click(fn=on_generate, inputs=gen_inputs, outputs=gen_outputs)

    # ── Save ──
    def on_save(audio_data, name, text):
        if audio_data is None:
            return t("vd_err_no_audio")
        try:
            dest = save_irodori_infer(audio_data, name, sample_text=text or "")
            return t("vd_ok_saved").format(dest)
        except Exception as e:
            logger.exception("Irodori infer save failed")
            return t("vd_err_save_fail").format(e)

    save_btn.click(fn=on_save, inputs=[state_audio, save_name, text_input], outputs=[status])

    def _on_tab_select():
        nums = list_kept_voice_numbers()
        ref_choices = [str(n) for n in nums]
        return (
            gr.update(choices=ref_choices, value=ref_choices[0] if ref_choices else None),
            gr.update(choices=[_LORA_NONE, *list_loras()]),
        )

    return {"refresh": _on_tab_select, "outputs": [shortcut_dropdown, lora_dropdown]}
