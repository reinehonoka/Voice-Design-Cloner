"""VoiceDesign: generate a new voice from a text prompt."""

import os
import re
from pathlib import Path
import soundfile as sf
from config import VOICE_DESIGN_DIR


_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def _sanitize_filename(name: str, default: str = "voice_design") -> str:
    """Convert arbitrary user input into a safe filename stem."""
    candidate = (name or "").strip()
    candidate = candidate.replace("\\", "_").replace("/", "_")
    candidate = _SAFE_NAME_RE.sub("_", candidate).strip("._")
    return candidate or default


def generate_voice_design(manager, text: str, instruct: str, **kwargs):
    """Generate a voice with VoiceDesign model. Returns (sample_rate, audio_array)."""
    manager.load_model("1.7B-VoiceDesign")
    wavs, sr = manager.current_model.generate_voice_design(
        text=text,
        language="auto",
        instruct=instruct,
        **kwargs,
    )
    return sr, wavs[0]


def save_voice(audio_tuple, name: str, sample_text: str = "") -> str:
    """Save audio data as a named voice file, plus a transcript txt.
    audio_tuple: (sr, numpy_array)."""
    sr, audio = audio_tuple
    os.makedirs(VOICE_DESIGN_DIR, exist_ok=True)
    safe_name = _sanitize_filename(name)
    dest = str(VOICE_DESIGN_DIR / f"{safe_name}.wav")
    if os.path.exists(dest):
        base, ext = os.path.splitext(dest)
        i = 1
        while os.path.exists(f"{base}_{i}{ext}"):
            i += 1
        dest = f"{base}_{i}{ext}"
    sf.write(dest, audio, sr, subtype="PCM_16")
    # Save transcript txt alongside wav
    txt_path = os.path.splitext(dest)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(sample_text)
    # Normalize to an absolute path for clearer status output.
    return str(Path(dest).resolve())


def list_kept_voices() -> list[str]:
    """List all kept voice files (full paths)."""
    os.makedirs(VOICE_DESIGN_DIR, exist_ok=True)
    return sorted(str(p) for p in VOICE_DESIGN_DIR.glob("*.wav"))


def list_kept_voice_numbers() -> list[int]:
    """List voice_design numbers from voice_design_*.wav files."""
    os.makedirs(VOICE_DESIGN_DIR, exist_ok=True)
    nums = []
    for p in VOICE_DESIGN_DIR.glob("voice_design*.wav"):
        m = re.search(r"voice_design_?(\d+)?\.wav$", p.name)
        if m:
            nums.append(int(m.group(1)) if m.group(1) else 0)
        elif p.name == "voice_design.wav":
            nums.append(0)
    return sorted(nums)


def get_kept_voice_path(num: int) -> str:
    """Get wav path for a voice_design number."""
    if num == 0:
        p = VOICE_DESIGN_DIR / "voice_design.wav"
    else:
        p = VOICE_DESIGN_DIR / f"voice_design_{num}.wav"
    return str(p) if p.exists() else None


def get_kept_voice_text(num: int) -> str:
    """Get transcript text for a voice_design number."""
    if num == 0:
        p = VOICE_DESIGN_DIR / "voice_design.txt"
    else:
        p = VOICE_DESIGN_DIR / f"voice_design_{num}.txt"
    if p.exists():
        return p.read_text(encoding="utf-8").strip()
    return ""
