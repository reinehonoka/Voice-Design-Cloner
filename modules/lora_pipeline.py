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
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

# Train and Irodori inference both grab the GPU and can OOM if run together.
# A single process-wide lock keeps them serialized. Callers outside this
# module should use ``gpu_session()``.
_GPU_LOCK = threading.Lock()


class GPUBusyError(RuntimeError):
    """Raised when another LoRA training or Irodori inference is in flight."""


class SubprocessFailed(RuntimeError):
    """Raised when an external Irodori command exits non-zero."""

    def __init__(self, cmd: list[str], returncode: int, stderr_tail: Iterable[str]):
        self.cmd = cmd
        self.returncode = returncode
        self.stderr_tail = tuple(stderr_tail)
        message = f"subprocess exited with code {returncode}: {' '.join(cmd)}"
        if self.stderr_tail:
            message += "\nlast stderr:\n" + "\n".join(self.stderr_tail)
        super().__init__(message)


def gpu_session():
    """Acquire the GPU lock non-blocking; release on context exit.

    Use as ``with gpu_session(): ...`` around any GPU-claiming work to make
    sure inference and training never overlap.
    """
    from contextlib import contextmanager

    @contextmanager
    def _cm():
        if not _GPU_LOCK.acquire(blocking=False):
            raise GPUBusyError(
                "Another GPU job is already running (LoRA training or Irodori "
                "inference). Wait for it to finish before starting a new one."
            )
        try:
            yield
        finally:
            _GPU_LOCK.release()

    return _cm()

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

    A single run can produce several intermediate ``checkpoint_*`` folders plus
    a ``checkpoint_final`` (or similar) at the end. We prefer:
      1. anything named like ``*final*`` or ``*last*``
      2. otherwise the newest ``adapter_model.safetensors`` by mtime

    Returns the path of the safetensors file (caller derives the directory).
    """
    candidates = list(folder.rglob("adapter_model.safetensors"))
    if not candidates:
        candidates = sorted(folder.rglob("*.safetensors"))
    if not candidates:
        return None

    def _is_final(p: Path) -> bool:
        parts = "/".join(p.parts).lower()
        return "final" in parts or "last" in parts

    final_first = sorted(
        candidates,
        key=lambda p: (0 if _is_final(p) else 1, -p.stat().st_mtime),
    )
    return final_first[0]


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
    """Yield stdout lines from a subprocess, mirroring stderr to logger.warning.

    Cancellation: when the generator is closed (Gradio cancel / GeneratorExit),
    the child is terminated, then killed if it doesn't exit promptly. Without
    this, training would keep holding the GPU after the user pressed Stop.
    """
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
    stderr_tail: deque[str] = deque(maxlen=50)

    def _drain_stderr(stream):
        for line in stream:
            text = line.rstrip()
            stderr_tail.append(text)
            logger.warning("[subprocess] %s", text)

    stderr_thread = threading.Thread(target=_drain_stderr, args=(proc.stderr,), daemon=True)
    stderr_thread.start()

    cancelled = False
    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            yield line.rstrip("\n")
    except GeneratorExit:
        cancelled = True
        raise
    finally:
        if proc.poll() is None:
            try:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
            except Exception:
                logger.exception("Failed to clean up subprocess")
        else:
            proc.wait()
        stderr_thread.join(timeout=2)
    if cancelled:
        return
    if proc.returncode != 0:
        raise SubprocessFailed(cmd, proc.returncode, stderr_tail)


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

    # Free up VRAM before training: an in-process Irodori worker would otherwise
    # compete with train.py for the same GPU. Also serialize concurrent invokes.
    if not _GPU_LOCK.acquire(blocking=False):
        raise GPUBusyError(
            "Another GPU job is already running (LoRA training or Irodori inference). "
            "Wait for it to finish."
        )
    try:
        from modules.irodori_bridge import get_bridge
        try:
            get_bridge().shutdown()
        except Exception:
            logger.exception("Failed to shut down Irodori worker before training")

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
        if manifest_path.exists():
            manifest_path.unlink()
        encode_error: SubprocessFailed | None = None
        encode_cmd = [
            str(py), str(encode_script),
            "--input-jsonl", str(jsonl_path),
            "--latent-dir", str(latent_dir),
            "--manifest", str(manifest_path),
        ]
        try:
            list(_stream_subprocess(encode_cmd, cwd=irodori_root))
        except SubprocessFailed as exc:
            encode_error = exc
        if not manifest_path.is_file():
            if encode_error is not None:
                raise RuntimeError(
                    f"encode_latents failed before producing manifest: {manifest_path}"
                ) from encode_error
            raise RuntimeError(f"encode_latents did not produce manifest: {manifest_path}")
        manifest_count = _count_nonempty_lines(manifest_path)
        if manifest_count == 0:
            message = (
                f"encode_latents wrote 0 entries to {manifest_path}. "
                "All audio files were rejected; check the [subprocess] logs above for skip reasons."
            )
            if encode_error is not None:
                raise RuntimeError(message) from encode_error
            raise RuntimeError(message)
        if encode_error is not None:
            if manifest_count < n_utts:
                raise RuntimeError(
                    f"encode_latents exited non-zero after writing only "
                    f"{manifest_count}/{n_utts} entries to {manifest_path}"
                ) from encode_error
            logger.warning(
                "encode_latents exited non-zero after writing %s/%s manifest entries; continuing",
                manifest_count, n_utts,
            )
            yield _stage(
                "encode_latents_warning",
                message=(
                    "Encoder exited non-zero after writing a complete manifest; "
                    "continuing to training."
                ),
                entries=manifest_count,
            )
        yield _stage(
            "encode_latents_done", manifest=str(manifest_path), entries=manifest_count,
        )

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
    finally:
        _GPU_LOCK.release()


def _count_nonempty_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


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
