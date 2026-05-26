"""LoRA fine-tuning pipeline for Irodori-TTS.

End-to-end: takes vdc's Voice Clone output (``output/{folder}/raw/*.wav`` +
``Neutral.txt``) and runs the three Irodori training stages — convert,
encode latents, train — using the Irodori venv as a subprocess.

UI calls :func:`run_lora_pipeline` and consumes the yielded progress events.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

from config import BASE_DIR, OUTPUT_DIR
from modules.irodori_bridge import _default_irodori_root

logger = logging.getLogger(__name__)

LORA_OUTPUT_DIR = OUTPUT_DIR / "lora"
LORA_DATA_DIR = OUTPUT_DIR / "lora_data"
INIT_CHECKPOINT_REPO = "Aratako/Irodori-TTS-500M-v3"
TRAIN_CONFIG_RELATIVE = Path("configs") / "train_500m_v3_lora.yaml"

# vdc esd lines look like ``0001|テキスト``. The Irodori lab format expects
# ``id: text`` per line under ``lab/{speaker}/{emotion}/{emotion}.txt``.
_ESD_LINE_RE = re.compile(r"^(?P<id>[^|]+)\|(?P<text>.+)$")

STEP_PRESETS: dict[str, int] = {
    "quick": 3000,
    "normal": 10000,
    "full": 30000,
}

# The shipped train_500m_v3_lora.yaml targets large-scale training (batch=80,
# 16 dataloader workers). For vdc's small clone datasets that combo wastes
# I/O and gives ~50 s/step on a 4060 Ti. Override per preset so quick runs
# actually feel quick.
PRESET_TRAIN_OVERRIDES: dict[str, dict[str, str]] = {
    "quick":  {"batch_size": "8",  "num_workers": "2"},
    "normal": {"batch_size": "16", "num_workers": "4"},
    "full":   {"batch_size": "32", "num_workers": "4"},
}


@dataclass
class LoraResult:
    speaker: str
    output_dir: Path
    adapter_path: Path | None


def list_clone_sources() -> list[str]:
    """Return ``output/`` subfolders that look like Voice Clone outputs."""
    if not OUTPUT_DIR.is_dir():
        return []
    sources: list[str] = []
    for entry in sorted(OUTPUT_DIR.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name in {"voice_design", "lora", "lora_data"}:
            continue
        raw = entry / "raw"
        if raw.is_dir() and any(raw.glob("*.wav")):
            sources.append(entry.name)
    return sources


def list_loras() -> list[str]:
    """Return available LoRA adapter speakers (folder names under output/lora/)."""
    if not LORA_OUTPUT_DIR.is_dir():
        return []
    return sorted(
        p.name
        for p in LORA_OUTPUT_DIR.iterdir()
        if p.is_dir() and _resolve_adapter_path(p) is not None
    )


def get_lora_training_wav(speaker: str) -> str | None:
    """Return a wav file from the LoRA's training data (lab/{speaker}/...).

    Used to auto-fill the reference audio when a LoRA is selected, since
    Irodori's clone mode requires ref_wav even with a trained adapter.
    """
    if not speaker:
        return None
    lab_speaker = LORA_DATA_DIR / "lab" / speaker
    if not lab_speaker.is_dir():
        return None
    for wavs_dir in lab_speaker.rglob("wavs"):
        if not wavs_dir.is_dir():
            continue
        wavs = sorted(wavs_dir.glob("*.wav"))
        if wavs:
            return str(wavs[0])
    return None


def get_lora_adapter_path(speaker: str) -> str | None:
    """Return the adapter *directory* for a saved LoRA, if any.

    Irodori's ``SamplingRequest.lora_adapter`` expects a PEFT adapter directory
    (containing ``adapter_model.safetensors`` + ``adapter_config.json``), not
    the safetensors file itself.
    """
    if not speaker:
        return None
    folder = LORA_OUTPUT_DIR / speaker
    if not folder.is_dir():
        return None
    found = _resolve_adapter_path(folder)
    return str(found.parent) if found is not None else None


def _resolve_adapter_path(folder: Path) -> Path | None:
    """train.py with --lora writes a PEFT adapter under output-dir.
    Find the actual checkpoint to pass back to inference."""
    # peft adapter_model.safetensors layout (newer)
    for cand in folder.rglob("adapter_model.safetensors"):
        return cand
    # Fallback: any *.safetensors in the folder
    for cand in sorted(folder.rglob("*.safetensors")):
        return cand
    return None


def _load_esd_lines(path: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        m = _ESD_LINE_RE.match(line)
        if not m:
            continue
        entries.append((m.group("id").strip(), m.group("text").strip()))
    return entries


def _find_esd_file(folder: Path) -> Path | None:
    """The clone tab saves a text list (default Neutral.txt) at the folder root."""
    # Prefer Neutral.txt; otherwise any single .txt sibling of raw/
    for cand in [folder / "Neutral.txt", folder / "esd.list"]:
        if cand.is_file():
            return cand
    txts = [p for p in folder.glob("*.txt") if p.is_file()]
    if len(txts) == 1:
        return txts[0]
    return None


def _stage(status: str, **extra) -> dict:
    return {"event": "stage", "status": status, **extra}


def _write_training_jsonl(
    *, lab_root: Path, speaker: str, emotion: str, out_jsonl: Path,
) -> int:
    """Walk lab/{speaker}/{emotion}/ and emit a HF-datasets-style JSONL.

    Output line shape::

        {"audio": "<absolute wav path>", "text": "<utterance text>"}
    """
    emotion_dir = lab_root / speaker / emotion
    txt_file = emotion_dir / f"{emotion}.txt"
    wavs_dir = emotion_dir / "wavs"
    if not txt_file.is_file():
        raise FileNotFoundError(f"{txt_file} not found")
    if not wavs_dir.is_dir():
        raise FileNotFoundError(f"{wavs_dir} not found")

    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with out_jsonl.open("w", encoding="utf-8") as out_f:
        for line in txt_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            file_id, text = line.split(":", 1)
            file_id = file_id.strip()
            text = text.strip()
            wav_path = wavs_dir / f"{file_id}.wav"
            if not wav_path.is_file():
                continue
            out_f.write(json.dumps(
                {"audio": str(wav_path.resolve()), "text": text},
                ensure_ascii=False,
            ) + "\n")
            written += 1
    if written == 0:
        raise ValueError(f"no entries produced from {txt_file}")
    return written


def _convert_clone_to_lab(
    *, source: Path, lab_root: Path, speaker: str, emotion: str
) -> int:
    """Translate vdc clone output into lab-format used by Irodori training.

    Returns the number of utterances exported.
    """
    raw_dir = source / "raw"
    if not raw_dir.is_dir():
        raise FileNotFoundError(f"missing raw/ under {source}")
    esd = _find_esd_file(source)
    if esd is None:
        raise FileNotFoundError(
            f"no text list (Neutral.txt / esd.list) found under {source}"
        )

    entries = _load_esd_lines(esd)
    if not entries:
        raise ValueError(f"text list {esd} has no usable lines")

    dest_dir = lab_root / speaker / emotion
    dest_wavs = dest_dir / "wavs"
    if dest_wavs.exists():
        shutil.rmtree(dest_wavs)
    dest_wavs.mkdir(parents=True, exist_ok=True)

    txt_lines: list[str] = []
    written = 0
    for file_id, text in entries:
        stem = file_id
        src_wav = raw_dir / f"{stem}.wav"
        if not src_wav.is_file():
            logger.warning("missing wav for id=%s under %s", stem, raw_dir)
            continue
        shutil.copy2(src_wav, dest_wavs / f"{stem}.wav")
        txt_lines.append(f"{stem}: {text}")
        written += 1

    if not written:
        raise ValueError(f"no wav/text pairs matched between {raw_dir} and {esd}")

    (dest_dir / f"{emotion}.txt").write_text("\n".join(txt_lines) + "\n", encoding="utf-8")
    return written


def _stream_subprocess(
    cmd: list[str], *, cwd: Path, env: dict | None = None
) -> Iterator[str]:
    """Yield stdout lines from a subprocess, mirroring stderr to logger.warning."""
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        env=env,
    )

    def _drain_stderr(stream):
        for line in stream:
            logger.warning("[subprocess] %s", line.rstrip())

    stderr_thread = threading.Thread(target=_drain_stderr, args=(proc.stderr,), daemon=True)
    stderr_thread.start()

    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            yield line.rstrip("\n")
    finally:
        proc.wait()
        stderr_thread.join(timeout=2)
    if proc.returncode != 0:
        raise RuntimeError(f"subprocess exited with code {proc.returncode}: {' '.join(cmd)}")


def _irodori_python() -> Path:
    root = _default_irodori_root()
    if sys.platform == "win32":
        return root / ".venv" / "Scripts" / "python.exe"
    return root / ".venv" / "bin" / "python"


def _ensure_init_checkpoint() -> Path:
    """Download (or reuse) the v3 base checkpoint used as ``--init-checkpoint``.

    We do this from the vdc venv so the user sees progress in the same console.
    """
    try:
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise RuntimeError(
            "huggingface_hub is not installed in the vdc venv. "
            "Re-run setup.bat to install dependencies."
        ) from exc
    path = hf_hub_download(repo_id=INIT_CHECKPOINT_REPO, filename="model.safetensors")
    return Path(path)


def _sanitize_speaker(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", (name or "").strip()).strip("._")
    return cleaned or "speaker"


def _resolve_steps(steps: int | str) -> int:
    if isinstance(steps, str):
        return STEP_PRESETS.get(steps.lower(), STEP_PRESETS["quick"])
    return int(steps)


def run_lora_pipeline(
    *,
    source: str | Path,
    speaker: str,
    steps: int | str = "quick",
    emotion: str = "neutral",
    batch_size: int | None = None,
    num_workers: int | None = None,
    learning_rate: float | None = None,
) -> Iterator[dict]:
    """Yield progress events while running the full LoRA pipeline.

    Yield shape::

        {"event": "stage", "status": "...", ...}
        {"event": "progress", "step": int, "max_steps": int, "loss": float | None}
        {"event": "done", "result": LoraResult, ...}
    """
    safe_speaker = _sanitize_speaker(speaker)
    max_steps = _resolve_steps(steps)
    source_dir = OUTPUT_DIR / source if isinstance(source, str) else Path(source)
    if not source_dir.is_dir():
        raise FileNotFoundError(f"source folder not found: {source_dir}")

    irodori_root = _default_irodori_root()
    py = _irodori_python()
    if not py.is_file():
        raise RuntimeError(
            f"Irodori venv python not found at {py}. Re-run setup.bat to install."
        )

    LORA_DATA_DIR.mkdir(parents=True, exist_ok=True)
    LORA_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    lab_root = LORA_DATA_DIR / "lab"
    jsonl_dir = LORA_DATA_DIR / "jsonl"
    latents_root = LORA_DATA_DIR / "latents"
    jsonl_dir.mkdir(parents=True, exist_ok=True)
    latents_root.mkdir(parents=True, exist_ok=True)

    # ── Stage 1: convert ──
    yield _stage("convert", message=f"Converting {source_dir.name} -> lab/{safe_speaker}/{emotion}")
    n_utts = _convert_clone_to_lab(
        source=source_dir, lab_root=lab_root, speaker=safe_speaker, emotion=emotion,
    )
    yield _stage("convert_done", utterances=n_utts)

    # ── Stage 2: create jsonl (pure file processing, runs in vdc venv) ──
    jsonl_path = jsonl_dir / f"{safe_speaker}.jsonl"
    yield _stage("create_jsonl", message=f"Writing {jsonl_path.name}")
    _write_training_jsonl(
        lab_root=lab_root, speaker=safe_speaker, emotion=emotion, out_jsonl=jsonl_path,
    )
    yield _stage("create_jsonl_done", jsonl=str(jsonl_path))

    # ── Stage 3: encode latents (runs in Irodori venv via subprocess) ──
    latent_dir = latents_root / safe_speaker
    manifest_path = LORA_DATA_DIR / "manifests" / f"{safe_speaker}_manifest.jsonl"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    encode_script = BASE_DIR / "modules" / "irodori_encode_latents.py"
    yield _stage("encode_latents", message="Encoding waveforms to latents")
    list(_stream_subprocess(
        [
            str(py), str(encode_script),
            "--input-jsonl", str(jsonl_path),
            "--latent-dir", str(latent_dir),
            "--manifest", str(manifest_path),
        ],
        cwd=irodori_root,
    ))
    if not manifest_path.is_file():
        raise RuntimeError(f"encode_latents did not produce manifest: {manifest_path}")
    yield _stage("encode_latents_done", manifest=str(manifest_path))

    # ── Stage 4: train ──
    yield _stage("init_checkpoint", message=f"Resolving init checkpoint ({INIT_CHECKPOINT_REPO})")
    init_ckpt = _ensure_init_checkpoint()
    yield _stage("init_checkpoint_done", checkpoint=str(init_ckpt))

    train_output_dir = LORA_OUTPUT_DIR / safe_speaker
    train_output_dir.mkdir(parents=True, exist_ok=True)
    train_config = irodori_root / TRAIN_CONFIG_RELATIVE
    if not train_config.is_file():
        raise RuntimeError(f"train config not found: {train_config}")

    preset_key = steps if isinstance(steps, str) else "quick"
    preset = PRESET_TRAIN_OVERRIDES.get(preset_key, PRESET_TRAIN_OVERRIDES["quick"])
    eff_batch = int(batch_size) if batch_size is not None else int(preset["batch_size"])
    eff_workers = int(num_workers) if num_workers is not None else int(preset["num_workers"])
    yield _stage(
        "train",
        message=f"Training LoRA ({max_steps} steps, batch={eff_batch})",
        max_steps=max_steps,
    )
    cmd = [
        str(py), str(irodori_root / "train.py"),
        "--config", str(train_config),
        "--manifest", str(manifest_path),
        "--init-checkpoint", str(init_ckpt),
        "--output-dir", str(train_output_dir),
        "--lora",
        "--max-steps", str(max_steps),
        "--batch-size", str(eff_batch),
        "--num-workers", str(eff_workers),
    ]
    if learning_rate is not None:
        cmd.extend(["--lr", str(float(learning_rate))])
    for line in _stream_subprocess(cmd, cwd=irodori_root):
        ev = _parse_train_line(line, max_steps)
        if ev is not None:
            yield ev

    adapter_path = _resolve_adapter_path(train_output_dir)
    yield {
        "event": "done",
        "speaker": safe_speaker,
        "output_dir": str(train_output_dir),
        "adapter_path": str(adapter_path) if adapter_path else None,
        "utterances": n_utts,
        "steps": max_steps,
    }


# train.py prints lines like ``[step 1234/30000] loss=0.5123 ...``. Parse what we
# can; anything we don't recognise becomes a generic status line so the UI can
# still surface it.
_STEP_RE = re.compile(
    r"step\s*[:=]?\s*(?P<step>\d+)\s*[/of]+\s*(?P<max>\d+)", re.IGNORECASE,
)
_LOSS_RE = re.compile(r"loss\s*[:=]?\s*(?P<loss>[0-9.]+(?:[eE][+-]?\d+)?)")


def _parse_train_line(line: str, max_steps: int) -> dict | None:
    if not line.strip():
        return None
    step_m = _STEP_RE.search(line)
    loss_m = _LOSS_RE.search(line)
    if step_m:
        step = int(step_m.group("step"))
        return {
            "event": "progress",
            "step": step,
            "max_steps": int(step_m.group("max")) or max_steps,
            "loss": float(loss_m.group("loss")) if loss_m else None,
            "raw": line,
        }
    return {"event": "log", "raw": line}
