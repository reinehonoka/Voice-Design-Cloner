"""Tools tab: resample WAVs and generate esd.list."""

import os
import glob
import time
import gradio as gr
import librosa
import soundfile as sf
from config import OUTPUT_DIR, VOICE_DESIGN_DIR

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
            gr.Markdown("### リサンプル")
            gr.Markdown("outputフォルダの raw/ 内WAVを一括リサンプルして resampled/ に出力します。")
            with gr.Group():
                resample_folder = gr.Dropdown(
                    choices=_list_output_folders(),
                    label="フォルダ選択",
                    interactive=True,
                )
                resample_sr = gr.Dropdown(
                    choices=[44100, 48000, 24000, 22050],
                    value=44100,
                    label="出力サンプルレート (Hz)",
                )
                resample_btn = gr.Button("リサンプル実行", variant="primary")
                resample_status = gr.Textbox(label="ステータス", interactive=False, lines=3)
            resample_refresh_btn = gr.Button("更新", variant="secondary")

        # ── Right: esd.list ──
        with gr.Column(scale=2):
            gr.Markdown("### esd.list 生成")
            gr.Markdown("outputフォルダを選択して raw/*.wav とテキストリストから esd.list を生成します。")
            with gr.Group():
                esd_folder = gr.Dropdown(
                    choices=_list_output_folders(),
                    label="フォルダ選択",
                    interactive=True,
                )
                speaker_name = gr.Textbox(
                    label="話者名（esd.listのspeaker列）",
                    placeholder="フォルダ名が自動入力されます",
                )
                esd_btn = gr.Button("esd.list 生成", variant="primary")
                esd_status = gr.Textbox(label="ステータス", interactive=False, lines=3)
            esd_refresh_btn = gr.Button("更新", variant="secondary")

    # ── Audio Info ──
    gr.HTML("<div style='height: 12px'></div>")
    gr.Markdown("### 音声情報")
    gr.Markdown("WAVファイルをアップロードして秒数・サンプルレートを確認します。")
    with gr.Group():
        info_files = gr.File(
            label="WAVファイル（複数可）",
            file_count="multiple",
            file_types=[".wav"],
        )
        audio_info = gr.Textbox(label="ファイル情報", interactive=False, lines=6)

    # ── Resample logic ──
    def on_resample_refresh():
        choices = _list_output_folders()
        return gr.update(choices=choices, value=choices[0] if choices else None)

    resample_refresh_btn.click(fn=on_resample_refresh, outputs=[resample_folder])

    def on_resample(folder, sr, progress=gr.Progress()):
        if not folder:
            return "エラー: フォルダを選択してください"
        sr = int(sr)
        base_dir = OUTPUT_DIR / folder
        raw_dir = base_dir / "raw"
        out_dir = base_dir / "resampled"
        if not raw_dir.exists():
            return f"エラー: {raw_dir} が見つかりません"
        wav_files = sorted(glob.glob(str(raw_dir / "*.wav")))
        if not wav_files:
            return "エラー: raw/ にWAVファイルがありません"
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
        return f"完了: {total}ファイルをリサンプル ({elapsed:.1f}秒)\n出力先: {out_dir}"

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
                bit_val = info.subtype  # e.g. "PCM_16"
                total_duration += dur
                sr_set.add(sr_val)
                ch_set.add(ch_val)
                bit_set.add(bit_val)
                ch_label = "モノラル" if ch_val == 1 else f"{ch_val}ch"
                bit_label = "16bit" if bit_val == "PCM_16" else "24bit" if bit_val == "PCM_24" else "32bit" if bit_val == "PCM_32" else bit_val
                lines.append(f"  {fname}: {dur:.1f}秒 / {sr_val}Hz / {ch_label} / {bit_label}")
            except Exception:
                lines.append(f"  {fname}: 読み取れません")
        header = f"ファイル数: {len(files)} / 合計: {total_duration:.1f}秒 ({total_duration / 60:.1f}分)"
        if len(sr_set) == 1 and len(ch_set) == 1 and len(bit_set) == 1:
            ch_label = "モノラル" if list(ch_set)[0] == 1 else f"{list(ch_set)[0]}ch"
            raw_bit = list(bit_set)[0]
            bit_label = "16bit" if raw_bit == "PCM_16" else "24bit" if raw_bit == "PCM_24" else "32bit" if raw_bit == "PCM_32" else raw_bit
            header += f"\n全ファイル一致: {list(sr_set)[0]}Hz / {ch_label} / {bit_label}"
        else:
            if len(sr_set) > 1:
                header += f"\n⚠ サンプルレート不一致: {sorted(sr_set)}"
            if len(ch_set) > 1:
                header += f"\n⚠ チャンネル数不一致: {sorted(ch_set)}"
            if len(bit_set) > 1:
                header += f"\n⚠ ビット深度不一致: {sorted(bit_set)}"
        return header + "\n" + "\n".join(lines)

    info_files.change(fn=on_files_change, inputs=[info_files], outputs=[audio_info])

    # ── esd.list logic ──
    def on_esd_refresh():
        choices = _list_output_folders()
        return gr.update(choices=choices, value=choices[0] if choices else None)

    esd_refresh_btn.click(fn=on_esd_refresh, outputs=[esd_folder])

    esd_folder.change(fn=lambda folder: folder or "", inputs=[esd_folder], outputs=[speaker_name])

    def on_generate_esd(folder, speaker):
        if not folder:
            return "エラー: フォルダを選択してください"
        base_dir = OUTPUT_DIR / folder
        if not base_dir.exists():
            return f"エラー: {base_dir} が存在しません"
        speaker = speaker.strip() or folder
        raw_dir = base_dir / "raw"
        if not raw_dir.exists():
            return f"エラー: {raw_dir} が見つかりません"
        wav_files = sorted(glob.glob(str(raw_dir / "*.wav")))
        if not wav_files:
            return "エラー: raw/ にWAVファイルがありません"
        # Load transcript: Neutral.txt — one line per file (line 1 = 0001.wav)
        # Also supports legacy esd.list format (filename|speaker|lang|text)
        txt_file = base_dir / "Neutral.txt"
        text_map = {}
        if txt_file.exists():
            with open(txt_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            for i, line in enumerate(lines):
                parts = line.split("|")
                if len(parts) >= 4:
                    # legacy esd.list format: 0001.wav|speaker|JP|text
                    text_map[parts[0]] = parts[3]
                elif len(parts) == 2:
                    # Neutral.txt format: 0001|text
                    text_map[parts[0] + ".wav"] = parts[1]
                else:
                    # plain text fallback: line index → 0001.wav
                    text_map[f"{i + 1:04d}.wav"] = line

        esd_lines = []
        skipped = []
        for wav_path in wav_files:
            fname = os.path.basename(wav_path)
            text = text_map.get(fname, "")
            if not text:
                skipped.append(fname)
                continue
            esd_lines.append(f"{fname}|{speaker}|JP|{text}")
        if not esd_lines:
            return "エラー: テキストが見つかりません。Neutral.txt等が必要です"
        esd_path = base_dir / "esd.list"
        with open(esd_path, "w", encoding="utf-8") as f:
            f.write("\n".join(esd_lines))
        msg = f"完了: {len(esd_lines)}行の esd.list を生成\n保存先: {esd_path}"
        if skipped:
            msg += f"\n⚠ テキスト未対応のためスキップ ({len(skipped)}件): {', '.join(skipped)}"
        return msg

    esd_btn.click(fn=on_generate_esd, inputs=[esd_folder, speaker_name], outputs=[esd_status])
