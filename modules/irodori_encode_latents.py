"""Standalone latent encoder for the LoRA pipeline.

Run inside the Irodori venv so it can import ``irodori_tts.codec``. The vdc
LoRA pipeline launches this via subprocess.

Reads a JSONL of ``{"audio": ..., "text": ...}`` entries, encodes each wav to
a DACVAE latent, and writes:

* ``{latent_dir}/{idx:08d}.pt`` for every successful entry
* ``{manifest}`` JSONL with ``{"text", "latent_path", "num_frames"}``

Usage::

    python irodori_encode_latents.py \\
        --input-jsonl path/to/foo.jsonl \\
        --latent-dir  path/to/latents/foo \\
        --manifest    path/to/foo_manifest.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Add CWD (Irodori root) to sys.path so the bundled irodori_tts package imports.
sys.path.insert(0, os.getcwd())

import torch  # noqa: E402

from irodori_tts.codec import DACVAECodec  # noqa: E402

TARGET_SR = 48000
NORMALIZE_DB = -16.0
CODEC_REPO = "Aratako/Semantic-DACVAE-Japanese-32dim"


def print_err(*args, **kwargs) -> None:
    kwargs.setdefault("file", sys.stderr)
    kwargs.setdefault("flush", True)
    print(*args, **kwargs)


def loudness_normalize(wav: torch.Tensor, target_db: float) -> torch.Tensor:
    rms = wav.pow(2).mean().sqrt().clamp_min(1e-8)
    current_db = 20 * torch.log10(rms)
    gain = 10 ** ((target_db - current_db) / 20)
    return (wav * gain).clamp(-1.0, 1.0)


def _load_wav(path: str, target_sr: int) -> torch.Tensor:
    """Load wav as mono float tensor at target_sr.

    Try torchaudio first (no extra dep); fall back to soundfile if torchaudio
    refuses the file (e.g. uncommon WAV subtypes on Windows).
    """
    try:
        import torchaudio
        wav, sr = torchaudio.load(path)
        if wav.size(0) > 1:
            wav = wav.mean(dim=0, keepdim=True)
        if sr != target_sr:
            wav = torchaudio.functional.resample(wav, orig_freq=sr, new_freq=target_sr)
        return wav.float()
    except Exception as torchaudio_exc:
        try:
            import numpy as np
            import soundfile as sf
            data, sr = sf.read(path, dtype="float32", always_2d=True)
            wav = torch.from_numpy(data.T)
            if wav.size(0) > 1:
                wav = wav.mean(dim=0, keepdim=True)
            if sr != target_sr:
                import torchaudio
                wav = torchaudio.functional.resample(wav, orig_freq=sr, new_freq=target_sr)
            return wav.float()
        except Exception as sf_exc:
            raise RuntimeError(
                f"both torchaudio and soundfile failed to load {path}: "
                f"torchaudio={torchaudio_exc} soundfile={sf_exc}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-jsonl", required=True)
    parser.add_argument("--latent-dir", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    input_path = Path(args.input_jsonl)
    latent_dir = Path(args.latent_dir)
    manifest_path = Path(args.manifest)

    latent_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    with input_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    print_err(f"[encode] {len(entries)} entries", flush=True)
    print_err(f"[encode] codec: {CODEC_REPO}", flush=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    codec = DACVAECodec.load(
        repo_id=CODEC_REPO,
        device=device,
        deterministic_encode=True,
        deterministic_decode=True,
        normalize_db=None,
    )

    written = 0
    skipped = 0
    with manifest_path.open("w", encoding="utf-8") as out_f:
        for i, entry in enumerate(entries):
            wav_path = entry["audio"]
            text = entry["text"]
            try:
                wav = _load_wav(wav_path, TARGET_SR)
                wav = loudness_normalize(wav, NORMALIZE_DB)
                with torch.inference_mode():
                    latent = codec.encode_waveform(wav, sample_rate=TARGET_SR)[0].cpu()
            except Exception as exc:
                print_err(f"[skip] {wav_path}: {exc}", flush=True)
                skipped += 1
                continue

            latent_name = f"{written:08d}.pt"
            latent_full = latent_dir / latent_name
            torch.save(latent, latent_full)

            rel = os.path.relpath(latent_full, start=manifest_path.parent)
            payload = {
                "text": text,
                "latent_path": rel.replace(os.sep, "/"),
                "num_frames": int(latent.shape[0]),
            }
            out_f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            written += 1
            if (i + 1) % 25 == 0 or i == len(entries) - 1:
                print_err(f"[encode] {i + 1}/{len(entries)}", flush=True)

    print_err(f"[done] written={written} skipped={skipped}", flush=True)
    if written == 0:
        print_err(
            "[error] no entries were encoded. Inspect the [skip] lines above to "
            "see why each wav was rejected.",
            flush=True,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
