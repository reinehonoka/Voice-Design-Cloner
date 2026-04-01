"""Voice Design tab: generate original voices from text prompts."""

import logging
import gradio as gr
from modules.voice_design import generate_voice_design, save_voice
from modules.translator import Translator
from modules.utils import load_presets
from config import DEFAULT_SAMPLE_TEXT

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
    presets_zh = load_presets("zh")
    presets_en = load_presets("en")

    with gr.Row():
        # ── Left: 1. Prompt + 2. Params ──
        with gr.Column(scale=3):
            gr.Markdown("### 1. ボイスプロンプト")
            gr.Markdown("生成したい声の特徴を記述（言語不問）")

            with gr.Group():
                instruct_text = gr.Textbox(
                    label="LLMプロンプト",
                    lines=5,
                    placeholder="例: 落ち着いた大人の女性の声、低めのトーン（日本語OK → 下のボタンで翻訳）",
                )

            with gr.Row():
                with gr.Column(scale=1, min_width=160):
                    translate_zh_btn = gr.Button("中国語に翻訳", variant="secondary")
                with gr.Column(scale=1, min_width=160):
                    translate_en_btn = gr.Button("英語に翻訳", variant="secondary")

            gr.HTML("<div style='height: 8px'></div>")

            with gr.Accordion("プリセットから選ぶ", open=False):
                with gr.Row():
                    preset_zh = gr.Dropdown(
                        choices=list(presets_zh.keys()),
                        label="中国語", value=None,
                    )
                    preset_en = gr.Dropdown(
                        choices=list(presets_en.keys()),
                        label="英語", value=None,
                    )
                    clear_preset_btn = gr.Button("クリア", size="sm", min_width=80)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown("### 2. 生成パラメータ")
            with gr.Group():
                temperature = gr.Slider(
                    minimum=0.1, maximum=1.0, step=0.05,
                    value=DEFAULTS["temperature"], label="Temperature（高い=表現豊か / 低い=安定）",
                )
                top_p = gr.Slider(
                    minimum=0.1, maximum=1.0, step=0.05,
                    value=DEFAULTS["top_p"], label="Top-P（低いほど品質安定）",
                )
                top_k = gr.Slider(
                    minimum=1, maximum=100, step=1,
                    value=DEFAULTS["top_k"], label="Top-K（候補トークン数）",
                )
                rep_penalty = gr.Slider(
                    minimum=1.0, maximum=1.5, step=0.01,
                    value=DEFAULTS["repetition_penalty"], label="繰り返しペナルティ",
                )
                reset_params_btn = gr.Button("デフォルトに戻す")

        # ── Right: 3. Sample text + 4. Preview + 5. Save ──
        with gr.Column(scale=2):
            gr.Markdown("### 3. 読み上げテキスト")
            gr.Markdown("この声で読み上げる文章")
            with gr.Group():
                sample_text = gr.Textbox(
                    label="読み上げテキスト",
                    value=DEFAULT_SAMPLE_TEXT,
                    lines=2,
                )

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown("### 4. プレビュー")
            with gr.Group():
                audio_preview = gr.Audio(label="プレビュー", type="numpy")
                status = gr.Textbox(label="ステータス", interactive=False)
                with gr.Row():
                    generate_btn = gr.Button("生成", variant="primary", scale=2)
                    reroll_btn = gr.Button("再生成", variant="secondary", scale=1)

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown("### 5. 保存")
            with gr.Group():
                save_name = gr.Textbox(label="保存名", value="voice_design")
                keep_btn = gr.Button("保存", variant="primary")

    state_path = gr.State()

    # ── Reset params ──
    reset_params_btn.click(
        fn=lambda: (DEFAULTS["temperature"], DEFAULTS["top_p"], DEFAULTS["top_k"], DEFAULTS["repetition_penalty"]),
        outputs=[temperature, top_p, top_k, rep_penalty],
    )

    # ── Translation (single step: clear presets + translate) ──
    def do_translate(text, lang):
        if not text.strip():
            return "テキストを入力してください", None, None
        try:
            result = translator.translate(text, lang)
            return result, None, None
        except Exception as e:
            logger.exception("Translation failed")
            return f"翻訳エラー: {e}", None, None

    translate_zh_btn.click(
        fn=lambda t: do_translate(t, "zh"), inputs=[instruct_text],
        outputs=[instruct_text, preset_zh, preset_en]
    )
    translate_en_btn.click(
        fn=lambda t: do_translate(t, "en"), inputs=[instruct_text],
        outputs=[instruct_text, preset_zh, preset_en]
    )

    # ── Presets ──
    def on_preset_zh(name):
        if not name:
            return gr.update(), gr.update()
        return presets_zh.get(name, ""), None

    def on_preset_en(name):
        if not name:
            return gr.update(), gr.update()
        return presets_en.get(name, ""), None

    preset_zh.change(fn=on_preset_zh, inputs=[preset_zh], outputs=[instruct_text, preset_en])
    preset_en.change(fn=on_preset_en, inputs=[preset_en], outputs=[instruct_text, preset_zh])
    clear_preset_btn.click(fn=lambda: (None, None, ""), outputs=[preset_zh, preset_en, instruct_text])

    # ── Generate ──
    def on_generate(instruct, sample, temp, tp, tk, rp):
        if not instruct.strip():
            return None, None, "ボイス指示が空です"
        try:
            sr, audio = generate_voice_design(
                manager, sample, instruct,
                temperature=temp, top_p=tp, top_k=int(tk), repetition_penalty=rp,
            )
            return (sr, audio), (sr, audio), f"生成完了 ({sr}Hz)"
        except Exception as e:
            logger.exception("Voice design generation failed")
            return None, None, f"エラー: {e}"

    gen_inputs = [instruct_text, sample_text, temperature, top_p, top_k, rep_penalty]
    gen_outputs = [audio_preview, state_path, status]

    generate_btn.click(fn=on_generate, inputs=gen_inputs, outputs=gen_outputs)
    reroll_btn.click(fn=on_generate, inputs=gen_inputs, outputs=gen_outputs)

    def on_keep(audio_data, name, sample):
        if audio_data is None:
            return "保存する音声がありません"
        try:
            dest = save_voice(audio_data, name, sample_text=sample)
            return f"保存完了: {dest}"
        except Exception as e:
            logger.exception("Voice save failed")
            return f"エラー: {e}"

    keep_btn.click(fn=on_keep, inputs=[state_path, save_name, sample_text], outputs=[status])
