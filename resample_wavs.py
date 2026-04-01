"""
Data/{speaker}/ 以下の全wavファイルのSRを確認し、
TARGET_SR (44100) でなければリサンプリングして上書きする。
"""

import argparse
import sys
from pathlib import Path

import librosa
import soundfile as sf

TARGET_SR = 44100


def resample_dir(speaker: str) -> None:
    data_dir = Path("Data") / speaker
    if not data_dir.exists():
        print(f"[ERROR] {data_dir} が見つかりません。")
        sys.exit(1)

    wav_files = list(data_dir.rglob("*.wav"))
    if not wav_files:
        print(f"[WARNING] {data_dir} にwavファイルがありません。")
        return

    resampled = 0
    for wav_path in wav_files:
        y, sr = librosa.load(str(wav_path), sr=None)
        if sr != TARGET_SR:
            print(f"  {wav_path.name}: {sr} Hz -> {TARGET_SR} Hz")
            y_resampled = librosa.resample(y, orig_sr=sr, target_sr=TARGET_SR)
            sf.write(str(wav_path), y_resampled, TARGET_SR)
            resampled += 1

    print(f"[INFO] {len(wav_files)} ファイル中 {resampled} ファイルをリサンプリングしました。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--speaker", required=True)
    args = parser.parse_args()
    resample_dir(args.speaker)
