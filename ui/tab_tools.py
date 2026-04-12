"""Tools tab: resample WAVs and generate esd.list."""

import os
import glob
import time
import gradio as gr
import librosa
import soundfile as sf
from config import OUTPUT_DIR, VOICE_DESIGN_DIR
from lang import t

_EXCLUDE_NAMES = {"voice_design", "_resampled"}


def _list_output_folders():
    if not OUTPUT_DIR.exists():
        return []
    folders = []
    for p in sorted(OUTPUT_DIR.iterdir()):
        if p.is_dir() and p.name not in _EXCLUDE_NAMES and p != VOICE_DESIGN_DIR:
            folders.append(p.name)
    return folders


def build_tools_tab():
    with gr.Row():
        # ── Left: Resample ──
        with gr.Column(scale=3):
            gr.Markdown(t("tools_resample_section"))
            gr.Markdown(t("tools_resample_desc"))
            with gr.Group():
                resample_folder = gr.Dropdown(
                    choices=_list_output_folders(),
                    label=t("tools_resample_folder_label"),
                    interactive=True,
                )
                resample_sr = gr.Dropdown(
                    choices=[44100, 48000, 24000, 22050],
                    value=44100,
                    label=t("tools_resample_sr_label"),
                )
                resample_btn = gr.Button(t("tools_btn_resample"), variant="primary")
                resample_status = gr.Textbox(label=t("tools_resample_status_label"), interactive=False, lines=3)
            resample_refresh_btn = gr.Button(t("tools_btn_resample_refresh"), variant="secondary")

        # ── Right: esd.list ──
        with gr.Column(scale=2):
            gr.Markdown(t("tools_esd_section"))
            gr.Markdown(t("tools_esd_desc"))
            with gr.Group():
                esd_folder = gr.Dropdown(
                    choices=_list_output_folders(),
                    label=t("tools_esd_folder_label"),
                    interactive=True,
                )
                speaker_name = gr.Textbox(
                    label=t("tools_esd_speaker_label"),
                    placeholder="",
                )
                esd_lang = gr.Dropdown(
                    choices=["JP", "EN", "ZH"],
                    value="JP",
                    label=t("tools_esd_lang_label"),
                )
                esd_btn = gr.Button(t("tools_btn_esd"), variant="primary")
                esd_status = gr.Textbox(label=t("tools_esd_status_label"), interactive=False, lines=3)
            esd_refresh_btn = gr.Button(t("tools_btn_esd_refresh"), variant="secondary")

    # ── Audio Info ──
    gr.HTML("<div style='height: 12px'></div>")
    gr.Markdown(t("tools_audio_info_section"))
    gr.Markdown(t("tools_audio_info_desc"))
    with gr.Group():
        info_files = gr.File(
            label=t("tools_audio_files_label"),
            file_count="multiple",
            file_types=[".wav"],
        )
        audio_info = gr.Textbox(label=t("tools_audio_info_label"), interactive=False, lines=6)

    # ── Resample logic ──
    def on_resample_refresh():
        choices = _list_output_folders()
        return gr.update(choices=choices, value=choices[0] if choices else None)

    resample_refresh_btn.click(fn=on_resample_refresh, outputs=[resample_folder])

    def on_resample(folder, sr, progress=gr.Progress()):
        if not folder:
            return t("tools_err_no_folder")
        sr = int(sr)
        base_dir = OUTPUT_DIR / folder
        raw_dir = base_dir / "raw"
        out_dir = base_dir / "resampled"
        if not raw_dir.exists():
            return t("tools_err_raw_not_found").format(raw_dir)
        wav_files = sorted(glob.glob(str(raw_dir / "*.wav")))
        if not wav_files:
            return t("tools_err_no_wavs")
        os.makedirs(str(out_dir), exist_ok=True)
        total = len(wav_files)
        start = time.time()
        for i, wav_path in enumerate(wav_files):
            fname = os.path.basename(wav_path)
            audio, orig_sr = librosa.load(wav_path, sr=None, mono=True)
            if orig_sr != sr:
                audio = librosa.resample(audio, orig_sr=orig_sr, target_sr=sr)
            sf.write(str(out_dir / fname), audio, sr, subtype="PCM_16")
            progress((i + 1) / total, f"{i + 1}/{total}")
        elapsed = time.time() - start
        return t("tools_resample_done").format(total, elapsed, out_dir)

    resample_btn.click(fn=on_resample, inputs=[resample_folder, resample_sr], outputs=[resample_status])

    # ── Audio info logic ──
    def on_files_change(files):
        if not files:
            return ""
        total_duration = 0.0
        lines = []
        sr_set = set()
        ch_set = set()
        bit_set = set()
        for f in files:
            path = f.name if hasattr(f, "name") else f
            fname = os.path.basename(path)
            try:
                info = sf.info(path)
                dur = info.duration
                sr_val = info.samplerate
                ch_val = info.channels
                bit_val = info.subtype
                total_duration += dur
                sr_set.add(sr_val)
                ch_set.add(ch_val)
                bit_set.add(bit_val)
                ch_label = t("tools_audio_mono") if ch_val == 1 else t("tools_audio_multi_ch").format(ch_val)
                bit_label = "16bit" if bit_val == "PCM_16" else "24bit" if bit_val == "PCM_24" else "32bit" if bit_val == "PCM_32" else bit_val
                lines.append(f"  {fname}: {dur:.1f}s / {sr_val}Hz / {ch_label} / {bit_label}")
            except Exception:
                lines.append(t("tools_audio_unreadable").format(fname))
        header = t("tools_audio_files").format(len(files), total_duration, total_duration / 60)
        if len(sr_set) == 1 and len(ch_set) == 1 and len(bit_set) == 1:
            ch_label = t("tools_audio_mono") if list(ch_set)[0] == 1 else t("tools_audio_multi_ch").format(list(ch_set)[0])
            raw_bit = list(bit_set)[0]
            bit_label = "16bit" if raw_bit == "PCM_16" else "24bit" if raw_bit == "PCM_24" else "32bit" if raw_bit == "PCM_32" else raw_bit
            header += t("tools_audio_all_match").format(list(sr_set)[0], ch_label, bit_label)
        else:
            if len(sr_set) > 1:
                header += t("tools_audio_sr_mismatch").format(sorted(sr_set))
            if len(ch_set) > 1:
                header += t("tools_audio_ch_mismatch").format(sorted(ch_set))
            if len(bit_set) > 1:
                header += t("tools_audio_bit_mismatch").format(sorted(bit_set))
        return header + "\n" + "\n".join(lines)

    info_files.change(fn=on_files_change, inputs=[info_files], outputs=[audio_info])

    # ── esd.list logic ──
    def on_esd_refresh():
        choices = _list_output_folders()
        return gr.update(choices=choices, value=choices[0] if choices else None)

    esd_refresh_btn.click(fn=on_esd_refresh, outputs=[esd_folder])

    esd_folder.change(fn=lambda folder: folder or "", inputs=[esd_folder], outputs=[speaker_name])

    def on_generate_esd(folder, speaker, lang_code):
        if not folder:
            return t("tools_err_no_folder")
        base_dir = OUTPUT_DIR / folder
        if not base_dir.exists():
            return t("tools_err_folder_not_exist").format(base_dir)
        speaker = speaker.strip() or folder
        raw_dir = base_dir / "raw"
        if not raw_dir.exists():
            return t("tools_err_raw_not_found").format(raw_dir)
        wav_files = sorted(glob.glob(str(raw_dir / "*.wav")))
        if not wav_files:
            return t("tools_err_no_wavs")
        txt_file = base_dir / "Neutral.txt"
        text_map = {}
        if txt_file.exists():
            with open(txt_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            for i, line in enumerate(lines):
                parts = line.split("|")
                if len(parts) >= 4:
                    text_map[parts[0]] = parts[3]
                elif len(parts) == 2:
                    text_map[parts[0] + ".wav"] = parts[1]
                else:
                    text_map[f"{i + 1:04d}.wav"] = line

        esd_lines = []
        skipped = []
        for wav_path in wav_files:
            fname = os.path.basename(wav_path)
            text = text_map.get(fname, "")
            if not text:
                skipped.append(fname)
                continue
            esd_lines.append(f"{fname}|{speaker}|{lang_code}|{text}")
        if not esd_lines:
            return t("tools_err_no_text")
        esd_path = base_dir / "esd.list"
        with open(esd_path, "w", encoding="utf-8") as f:
            f.write("\n".join(esd_lines))
        msg = t("tools_esd_done").format(len(esd_lines), esd_path)
        if skipped:
            msg += t("tools_esd_skip").format(len(skipped), ", ".join(skipped))
        return msg

    esd_btn.click(fn=on_generate_esd, inputs=[esd_folder, speaker_name, esd_lang], outputs=[esd_status])
