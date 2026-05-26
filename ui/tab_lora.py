"""LoRA tab: fine-tune Irodori-TTS on a Voice Clone output folder."""

import logging
import gradio as gr

from lang import t
from modules.lora_pipeline import (
    LORA_OUTPUT_DIR,
    PRESET_TRAIN_OVERRIDES,
    STEP_PRESETS,
    list_clone_sources,
    list_loras,
    run_lora_pipeline,
)
from modules.model_manager import ModelManager

logger = logging.getLogger(__name__)


def build_lora_tab(manager: ModelManager):
    # LoRA training runs in an Irodori subprocess regardless of which backend
    # vdc itself is using, so this tab stays fully interactive even when the
    # active backend is Qwen3 / faster. The trained adapter only becomes
    # usable in the Voice Clone / Inference tabs after switching to Irodori,
    # which is noted in the manual.
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown(t("lora_source_section"))
            with gr.Group():
                source_dropdown = gr.Dropdown(
                    choices=list_clone_sources(),
                    label=t("lora_source_label"),
                )
                refresh_source_btn = gr.Button(t("lora_btn_refresh"), variant="secondary")

            gr.HTML("<div style='height: 12px'></div>")

            gr.Markdown(t("lora_settings_section"))
            with gr.Group():
                speaker_name = gr.Textbox(
                    label=t("lora_speaker_label"),
                    placeholder="honoka",
                )
                steps_radio = gr.Radio(
                    choices=[(f"{k} ({v})", k) for k, v in STEP_PRESETS.items()],
                    value="quick",
                    label=t("lora_steps_label"),
                )
                with gr.Accordion(t("lora_advanced_section"), open=False):
                    steps_override = gr.Number(
                        label=t("lora_steps_override_label"),
                        value=STEP_PRESETS["quick"], precision=0,
                    )
                    batch_size = gr.Number(
                        label=t("lora_batch_label"),
                        value=int(PRESET_TRAIN_OVERRIDES["quick"]["batch_size"]),
                        precision=0,
                    )
                    num_workers = gr.Number(
                        label=t("lora_workers_label"),
                        value=int(PRESET_TRAIN_OVERRIDES["quick"]["num_workers"]),
                        precision=0,
                    )
                    learning_rate = gr.Number(
                        label=t("lora_lr_label"),
                        value=0.0001,
                    )

        with gr.Column(scale=2):
            gr.Markdown(t("lora_existing_section"))
            with gr.Group():
                existing_list = gr.Textbox(
                    value="\n".join(list_loras()) or t("lora_existing_none"),
                    label=t("lora_existing_label"),
                    interactive=False,
                    lines=5,
                )
                refresh_existing_btn = gr.Button(t("lora_btn_refresh"), variant="secondary")

            gr.HTML("<div style='height: 12px'></div>")

            with gr.Row():
                start_btn = gr.Button(t("lora_btn_start"), variant="primary", scale=3)
                stop_btn = gr.Button(t("lora_btn_stop"), variant="secondary", scale=1)

            gr.Markdown(t("lora_progress_section"))
            with gr.Group():
                status_text = gr.Textbox(label=t("lora_status_label"), interactive=False)
                log_text = gr.Textbox(label=t("lora_log_label"), interactive=False, lines=12)

    # ── refresh handlers ──
    refresh_source_btn.click(
        fn=lambda: gr.update(choices=list_clone_sources()),
        outputs=[source_dropdown],
    )
    refresh_existing_btn.click(
        fn=lambda: "\n".join(list_loras()) or t("lora_existing_none"),
        outputs=[existing_list],
    )

    # ── preset radio updates the advanced overrides to its defaults ──
    def _on_preset_change(preset):
        steps = STEP_PRESETS.get(preset, STEP_PRESETS["quick"])
        overrides = PRESET_TRAIN_OVERRIDES.get(preset, PRESET_TRAIN_OVERRIDES["quick"])
        return steps, int(overrides["batch_size"]), int(overrides["num_workers"])

    steps_radio.change(
        fn=_on_preset_change,
        inputs=[steps_radio],
        outputs=[steps_override, batch_size, num_workers],
    )

    # ── start training ──
    def on_start(source, speaker, steps, steps_n, batch, workers, lr):
        if not source:
            yield t("lora_err_no_source"), ""
            return
        if not speaker or not speaker.strip():
            yield t("lora_err_no_speaker"), ""
            return

        # Explicit step count from the advanced field wins over the preset.
        effective_steps = int(steps_n) if steps_n and int(steps_n) > 0 else steps
        log_buffer: list[str] = []
        try:
            for event in run_lora_pipeline(
                source=source,
                speaker=speaker.strip(),
                steps=effective_steps,
                batch_size=int(batch) if batch else None,
                num_workers=int(workers) if workers is not None else None,
                learning_rate=float(lr) if lr else None,
            ):
                kind = event.get("event")
                if kind == "stage":
                    line = f"[{event['status']}] {event.get('message', '')}"
                    log_buffer.append(line)
                    yield line, "\n".join(log_buffer[-50:])
                elif kind == "progress":
                    step = event.get("step", 0)
                    max_s = event.get("max_steps", 0)
                    loss = event.get("loss")
                    line = f"step {step}/{max_s}" + (f"  loss={loss:.4f}" if loss is not None else "")
                    yield line, "\n".join(log_buffer[-49:] + [line])
                elif kind == "log":
                    raw = event.get("raw", "")
                    log_buffer.append(raw)
                    yield "", "\n".join(log_buffer[-50:])
                elif kind == "done":
                    summary = t("lora_ok_done").format(
                        event.get("speaker"), event.get("output_dir"),
                    )
                    log_buffer.append(summary)
                    yield summary, "\n".join(log_buffer[-50:])
        except Exception as e:
            logger.exception("LoRA pipeline failed")
            log_buffer.append(f"ERROR: {e}")
            yield t("lora_err_failed").format(e), "\n".join(log_buffer[-50:])

    train_event = start_btn.click(
        fn=on_start,
        inputs=[
            source_dropdown, speaker_name, steps_radio,
            steps_override, batch_size, num_workers, learning_rate,
        ],
        outputs=[status_text, log_text],
    )
    stop_btn.click(fn=None, cancels=[train_event])

    def _refresh_on_select():
        return (
            gr.update(choices=list_clone_sources()),
            "\n".join(list_loras()) or t("lora_existing_none"),
        )

    return {"refresh": _refresh_on_select, "outputs": [source_dropdown, existing_list]}

    def _on_tab_select():
        return (
            gr.update(choices=list_clone_sources()),
            "\n".join(list_loras()) or t("lora_existing_none"),
        )

    return {"refresh": _on_tab_select, "outputs": [source_dropdown, existing_list]}
