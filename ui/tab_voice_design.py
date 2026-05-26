"""Voice Design tab: generate original voices from text prompts."""

import logging
import gradio as gr
from modules.voice_design import generate_voice_design, save_voice, TTS_LANGUAGES
from modules.translator import Translator
from modules.utils import load_presets_localized
from config import DEFAULT_SAMPLE_TEXT, TTS_LANG
from lang import t

translator = Translator()
translator.preload()
logger = logging.getLogger(__name__)

DEFAULTS = {
    "temperature": 0.9,
    "top_p": 1.0,
    "top_k": 50,
    "repetition_penalty": 1.05,
}


def build_voice_design_tab(manager):
    presets_ja = load_presets_localized("ja")
    presets_zh = load_presets_localized("zh")
    presets_en = load_presets_localized("en")

    # Irodori-TTS is Japanese-only and uses a diffusion sampler whose params
    # don't map to the Qwen-style temperature / top-p / top-k controls.
    # When that backend is active we lock everything that wouldn't apply.
    is_irodori = manager.backend == "irodori"
    qwen_interactive = not is_irodori

    with gr.Row():
        # ── Left: 1. Prompt + 2. Params ──
        with gr.Column(scale=3):
            gr.Markdown(t("vd_prompt_section"))
            gr.Markdown(t("vd_prompt_desc"))

            with gr.Group():
                instruct_text = gr.Textbox(
                    label=t("vd_prompt_label"),
                    lines=5,
                    placeholder=t("vd_prompt_placeholder"),
                )

            with gr.Row():
                with gr.Column(scale=1, min_width=120):
                    translate_ja_btn = gr.Button(t("vd_btn_translate_ja"), variant="secondary", interactive=qwen_interactive)
                with gr.Column(scale=1, min_width=120):
                    translate_zh_btn = gr.Button(t("vd_btn_translate_zh"), variant="secondary", interactive=qwen_interactive)
                with gr.Column(scale=1, min_width=120):
                    translate_en_btn = gr.Button(t("vd_btn_translate_en"), variant="secondary", interactive=qwen_interactive)

            gr.HTML("<div style='height: 8px'></div>")

            with gr.Accordion(t("vd_preset_accordion"), open=False):
                with gr.Row():
                    preset_ja = gr.Dropdown(
                        choices=list(presets_ja.keys()),
                        label=t("vd_preset_ja_label"), value=None,
                    )
                    preset_zh = gr.Dropdown(
                        choices=list(presets_zh.keys()),
                        label=t("vd_preset_zh_label"), value=None,
                        interactive=qwen_interactive,
                    )
                    preset_en = gr.Dropdown(
                        choices=list(presets_en.keys()),
                        label=t("vd_preset_en_label"), value=None,
                        interactive=qwen_interactive,
                    )
                    clear_preset_btn = gr.Button(t("vd_btn_clear_preset"), size="sm", min_width=80)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("vd_params_section"))
            with gr.Group():
                temperature = gr.Slider(
                    minimum=0.1, maximum=1.0, step=0.05,
                    value=DEFAULTS["temperature"], label=t("vd_temperature_label"),
                    interactive=qwen_interactive,
                )
                top_p = gr.Slider(
                    minimum=0.1, maximum=1.0, step=0.05,
                    value=DEFAULTS["top_p"], label=t("vd_top_p_label"),
                    interactive=qwen_interactive,
                )
                top_k = gr.Slider(
                    minimum=1, maximum=100, step=1,
                    value=DEFAULTS["top_k"], label=t("vd_top_k_label"),
                    interactive=qwen_interactive,
                )
                rep_penalty = gr.Slider(
                    minimum=1.0, maximum=1.5, step=0.01,
                    value=DEFAULTS["repetition_penalty"], label=t("vd_rep_penalty_label"),
                    interactive=qwen_interactive,
                )
                reset_params_btn = gr.Button(t("vd_btn_reset_params"), interactive=qwen_interactive)

        # ── Right: 3. Sample text + 4. Preview + 5. Save ──
        with gr.Column(scale=2):
            gr.Markdown(t("vd_sample_section"))
            gr.Markdown(t("vd_sample_desc"))
            with gr.Group():
                sample_text = gr.Textbox(
                    label=t("vd_sample_label"),
                    value=DEFAULT_SAMPLE_TEXT,
                    lines=2,
                )
                tts_lang_dropdown = gr.Dropdown(
                    choices=(["japanese"] if is_irodori else TTS_LANGUAGES),
                    value=("japanese" if is_irodori else TTS_LANG),
                    label=t("vd_tts_lang_label"),
                    interactive=qwen_interactive,
                )

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("vd_preview_section"))
            with gr.Group():
                audio_preview = gr.Audio(label=t("vd_preview_label"), type="numpy")
                status = gr.Textbox(label=t("vd_status_label"), interactive=False)
                with gr.Row():
                    generate_btn = gr.Button(t("vd_btn_generate"), variant="primary", scale=2)
                    reroll_btn = gr.Button(t("vd_btn_reroll"), variant="secondary", scale=1)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("vd_save_section"))
            with gr.Group():
                save_name = gr.Textbox(label=t("vd_save_name_label"), value="voice_design")
                keep_btn = gr.Button(t("vd_btn_save"), variant="primary")

    state_path = gr.State()

    # ── Reset params ──
    reset_params_btn.click(
        fn=lambda: (DEFAULTS["temperature"], DEFAULTS["top_p"], DEFAULTS["top_k"], DEFAULTS["repetition_penalty"]),
        outputs=[temperature, top_p, top_k, rep_penalty],
    )

    # ── Translation ──
    def do_translate(text, lang):
        if not text.strip():
            return t("vd_err_translate_empty"), None, None, None
        try:
            result = translator.translate(text, lang)
            return result, None, None, None
        except Exception as e:
            logger.exception("Translation failed")
            return t("vd_err_translate_fail").format(e), None, None, None

    translate_ja_btn.click(
        fn=lambda text: do_translate(text, "ja"), inputs=[instruct_text],
        outputs=[instruct_text, preset_ja, preset_zh, preset_en]
    )
    translate_zh_btn.click(
        fn=lambda text: do_translate(text, "zh"), inputs=[instruct_text],
        outputs=[instruct_text, preset_ja, preset_zh, preset_en]
    )
    translate_en_btn.click(
        fn=lambda text: do_translate(text, "en"), inputs=[instruct_text],
        outputs=[instruct_text, preset_ja, preset_zh, preset_en]
    )

    # ── Presets ──
    def on_preset_ja(name):
        if not name:
            return gr.update(), gr.update(), gr.update()
        return presets_ja.get(name, ""), None, None

    def on_preset_zh(name):
        if not name:
            return gr.update(), gr.update(), gr.update()
        return presets_zh.get(name, ""), None, None

    def on_preset_en(name):
        if not name:
            return gr.update(), gr.update(), gr.update()
        return presets_en.get(name, ""), None, None

    preset_ja.change(fn=on_preset_ja, inputs=[preset_ja], outputs=[instruct_text, preset_zh, preset_en])
    preset_zh.change(fn=on_preset_zh, inputs=[preset_zh], outputs=[instruct_text, preset_ja, preset_en])
    preset_en.change(fn=on_preset_en, inputs=[preset_en], outputs=[instruct_text, preset_ja, preset_zh])
    clear_preset_btn.click(fn=lambda: (None, None, None, ""), outputs=[preset_ja, preset_zh, preset_en, instruct_text])

    # ── Generate ──
    def on_generate(instruct, sample, lang, temp, tp, tk, rp):
        if not instruct.strip():
            return None, None, t("vd_err_empty_prompt")
        try:
            sr, audio = generate_voice_design(
                manager, sample, instruct, language=lang,
                temperature=temp, top_p=tp, top_k=int(tk), repetition_penalty=rp,
            )
            return (sr, audio), (sr, audio), t("vd_ok_generated").format(sr)
        except Exception as e:
            logger.exception("Voice design generation failed")
            return None, None, t("vd_err_generate_fail").format(e)

    gen_inputs = [instruct_text, sample_text, tts_lang_dropdown, temperature, top_p, top_k, rep_penalty]
    gen_outputs = [audio_preview, state_path, status]

    generate_btn.click(fn=on_generate, inputs=gen_inputs, outputs=gen_outputs)
    reroll_btn.click(fn=on_generate, inputs=gen_inputs, outputs=gen_outputs)

    def on_keep(audio_data, name, sample):
        if audio_data is None:
            return t("vd_err_no_audio")
        try:
            dest = save_voice(audio_data, name, sample_text=sample)
            return t("vd_ok_saved").format(dest)
        except Exception as e:
            logger.exception("Voice save failed")
            return t("vd_err_save_fail").format(e)

    keep_btn.click(fn=on_keep, inputs=[state_path, save_name, sample_text], outputs=[status])
