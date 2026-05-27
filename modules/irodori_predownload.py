"""Pre-download Irodori-TTS model assets during setup."""

from __future__ import annotations

import os

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

from huggingface_hub import hf_hub_download, snapshot_download


CHECKPOINTS = (
    ("Aratako/Irodori-TTS-500M-v2-VoiceDesign", "model.safetensors"),
    ("Aratako/Irodori-TTS-500M-v3", "model.safetensors"),
)

CODEC_REPO = "Aratako/Semantic-DACVAE-Japanese-32dim"


def main() -> int:
    print("[INFO] Pre-downloading Irodori-TTS model assets...")
    for repo_id, filename in CHECKPOINTS:
        print(f"[INFO] Downloading/checking {repo_id}/{filename}")
        hf_hub_download(repo_id=repo_id, filename=filename)

    print(f"[INFO] Downloading/checking {CODEC_REPO}")
    snapshot_download(repo_id=CODEC_REPO)
    print("[INFO] Irodori-TTS model assets are ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
