"""Irodori-TTS persistent worker.

Runs inside the Irodori venv (located at %USERPROFILE%\\.vdc-engines\\Irodori-TTS\\.venv\\).
The vdc main process launches this via subprocess with CWD set to the Irodori
project root so the ``irodori_tts`` package imports cleanly.

Protocol: newline-delimited JSON on stdin/stdout.

Requests::

    {"op": "synthesize", "mode": "design", "text": "...", "caption": "...",
     "out_path": "...", "seed": null}
    {"op": "synthesize", "mode": "clone",  "text": "...", "ref_wav": "...",
     "caption": null, "out_path": "...", "seed": null,
     "target_sr": 44100}
    {"op": "shutdown"}

Responses::

    {"ok": true, "out_path": "...", "sample_rate": 48000, "used_seed": 12345}
    {"ok": false, "error": "..."}
"""

from __future__ import annotations

import json
import os
import sys
import traceback
from pathlib import Path
from typing import Any

# vdc launches this worker with CWD set to the Irodori-TTS project root so the
# bundled ``irodori_tts`` package is importable. Python doesn't add CWD to
# sys.path automatically when running a script outside of it, so do it here.
sys.path.insert(0, os.getcwd())
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

# Force stdin/stdout/stderr to UTF-8. The bridge writes UTF-8 JSON on stdin,
# but on Japanese Windows the default Python text-mode encoding is cp932,
# which would mangle non-ASCII characters into surrogates and break the
# HF tokenizer downstream. reconfigure() is available on Python >= 3.7.
sys.stdin.reconfigure(encoding="utf-8", errors="strict")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Irodori (and friends like huggingface_hub / torch / DAC codec) print
# diagnostics, timings, and download progress to stdout. The bridge uses
# stdout as a JSON line protocol, so any rogue print would corrupt the
# protocol. Capture the real stdout for our own use and redirect Python's
# sys.stdout to stderr so every imported library logs there instead.
_PROTOCOL_STDOUT = sys.stdout
sys.stdout = sys.stderr

from huggingface_hub import hf_hub_download  # noqa: E402

from irodori_tts.inference_runtime import (  # noqa: E402
    InferenceRuntime,
    RuntimeKey,
    SamplingRequest,
    default_runtime_device,
    save_wav,
)

CHECKPOINTS = {
    "design": "Aratako/Irodori-TTS-500M-v2-VoiceDesign",
    "clone": "Aratako/Irodori-TTS-500M-v3",
}

CODEC_REPO = "Aratako/Semantic-DACVAE-Japanese-32dim"


def _log(message: str) -> None:
    print(f"[Irodori] {message}", file=sys.stderr, flush=True)


class WorkerState:
    def __init__(self) -> None:
        self.runtime: InferenceRuntime | None = None
        self.mode: str | None = None

    def ensure_runtime(self, mode: str) -> InferenceRuntime:
        if self.runtime is not None and self.mode == mode:
            _log(f"Runtime already loaded for mode={mode}.")
            return self.runtime
        if self.runtime is not None:
            _log(f"Unloading runtime for mode={self.mode}.")
            del self.runtime
            self.runtime = None
            import gc
            import torch
            torch.cuda.empty_cache()
            gc.collect()
        repo = CHECKPOINTS[mode]
        _log(f"Preparing runtime for mode={mode}.")
        _log(f"Checking/downloading checkpoint: {repo}/model.safetensors")
        ckpt = hf_hub_download(repo_id=repo, filename="model.safetensors")
        device = default_runtime_device()
        _log(f"Loading Irodori runtime on device={device}.")
        self.runtime = InferenceRuntime.from_key(
            RuntimeKey(
                checkpoint=ckpt,
                model_device=device,
                codec_repo=CODEC_REPO,
                model_precision="fp32",
                codec_device=device,
                codec_precision="fp32",
                codec_deterministic_encode=True,
                codec_deterministic_decode=True,
                compile_model=False,
                compile_dynamic=False,
            )
        )
        self.mode = mode
        _log(f"Runtime ready for mode={mode}.")
        return self.runtime


def _save_wav_resampled(path: Path, audio, src_sr: int, target_sr: int | None) -> None:
    if target_sr is None or target_sr == src_sr:
        save_wav(path, audio, src_sr)
        return
    # Resample via torchaudio (already a direct dep of Irodori-TTS) rather
    # than librosa, which isn't pinned in Irodori's pyproject.
    import numpy as np
    import soundfile as sf
    import torch
    import torchaudio
    wav = audio.squeeze().detach().cpu()
    if wav.dim() == 1:
        wav = wav.unsqueeze(0)
    resampled = torchaudio.functional.resample(
        wav, orig_freq=int(src_sr), new_freq=int(target_sr),
    )
    sf.write(str(path), resampled.squeeze(0).numpy().astype(np.float32), int(target_sr))


def handle_synthesize(state: WorkerState, req: dict[str, Any]) -> dict[str, Any]:
    mode = req["mode"]
    if mode not in CHECKPOINTS:
        return {"ok": False, "error": f"unknown mode: {mode}"}

    _log(f"Synthesis requested: mode={mode}.")
    runtime = state.ensure_runtime(mode)

    text = req["text"]
    out_path = Path(req["out_path"])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    target_sr = req.get("target_sr")

    sampling = SamplingRequest(
        text=text,
        caption=req.get("caption"),
        ref_wav=req.get("ref_wav") if mode == "clone" else None,
        ref_latent=None,
        no_ref=(mode == "design"),
        ref_normalize_db=-16.0,
        ref_ensure_max=True,
        num_candidates=1,
        decode_mode="sequential",
        # v3 (clone) has an auto Duration Predictor and prefers seconds=None.
        # v2-VoiceDesign (design) does not, so fix it at 30.0 like
        # master/design/voice_design.py.
        seconds=(30.0 if mode == "design" else None),
        max_ref_seconds=30.0,
        lora_adapter=req.get("lora_path"),
        max_text_len=None,
        max_caption_len=None,
        num_steps=40,
        cfg_scale_text=3.0,
        cfg_scale_caption=3.0,
        cfg_scale_speaker=5.0,
        cfg_guidance_mode="independent",
        cfg_scale=None,
        cfg_min_t=0.5,
        cfg_max_t=1.0,
        truncation_factor=None,
        rescale_k=None,
        rescale_sigma=None,
        context_kv_cache=True,
        speaker_kv_scale=None,
        speaker_kv_min_t=None,
        speaker_kv_max_layers=None,
        seed=req.get("seed"),
        trim_tail=True,
        tail_window_size=20,
        tail_std_threshold=0.05,
        tail_mean_threshold=0.1,
    )

    _log("Generating audio...")
    result = runtime.synthesize(sampling, log_fn=lambda msg: _log(str(msg)))
    _log(f"Saving wav: {out_path}")
    _save_wav_resampled(out_path, result.audio, result.sample_rate, target_sr)
    _log("Synthesis complete.")
    return {
        "ok": True,
        "out_path": str(out_path),
        "sample_rate": target_sr or result.sample_rate,
        "used_seed": result.used_seed,
    }


def _emit(payload: dict[str, Any]) -> None:
    _PROTOCOL_STDOUT.write(json.dumps(payload, ensure_ascii=False) + "\n")
    _PROTOCOL_STDOUT.flush()


def main() -> int:
    state = WorkerState()
    _emit({"ok": True, "event": "ready"})

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            req = json.loads(raw)
        except json.JSONDecodeError as exc:
            _emit({"ok": False, "error": f"invalid json: {exc}"})
            continue

        op = req.get("op")
        if op == "shutdown":
            _emit({"ok": True, "event": "shutdown"})
            return 0
        if op == "synthesize":
            try:
                _emit(handle_synthesize(state, req))
            except Exception as exc:
                _emit({"ok": False, "error": f"{type(exc).__name__}: {exc}",
                       "trace": traceback.format_exc()})
            continue
        _emit({"ok": False, "error": f"unknown op: {op}"})

    return 0


if __name__ == "__main__":
    sys.exit(main())
