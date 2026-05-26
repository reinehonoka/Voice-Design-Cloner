"""VoiceDesign: generate a new voice from a text prompt."""

import os
import re
import tempfile
from pathlib import Path
import soundfile as sf
from config import VOICE_DESIGN_DIR, TTS_LANG

TTS_LANGUAGES = [
    "japanese", "english", "chinese", "korean",
    "german", "french", "spanish", "italian",
    "portuguese", "russian",
]


_SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def _sanitize_filename(name: str, default: str = "voice_design") -> str:
    """Convert arbitrary user input into a safe filename stem."""
    candidate = (name or "").strip()
    candidate = candidate.replace("\\", "_").replace("/", "_")
    candidate = _SAFE_NAME_RE.sub("_", candidate).strip("._")
    return candidate or default


def generate_voice_design(manager, text: str, instruct: str, language: str | None = None, **kwargs):
    """Generate a voice with VoiceDesign model. Returns (sample_rate, audio_array)."""
    if manager.backend == "irodori":
        return _generate_voice_design_irodori(text, instruct)
    manager.load_model("1.7B-VoiceDesign")
    wavs, sr = manager.current_model.generate_voice_design(
        text=text,
        language=language or TTS_LANG,
        instruct=instruct,
        **kwargs,
    )
    return sr, wavs[0]


def _generate_voice_design_irodori(text: str, caption: str):
    """Run the Irodori worker once for VoiceDesign and return (sr, audio)."""
    from modules.irodori_bridge import get_bridge
    from modules.lora_pipeline import gpu_session
    bridge = get_bridge()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        out_path = tmp.name
    try:
        with gpu_session():
            bridge.synthesize(mode="design", text=text, caption=caption, out_path=out_path)
        audio, sr = sf.read(out_path, dtype="float32")
        return sr, audio
    finally:
        try:
            os.remove(out_path)
        except OSError:
            pass


def generate_clone_oneshot_irodori(
    *,
    text: str,
    ref_wav: str,
    caption: str | None = None,
    lora_path: str | None = None,
    seed: int | None = None,
):
    """One-shot Irodori clone (mode=clone, single utterance) for the Inference tab.

    Returns (sample_rate, audio_array). The worker writes to a temp wav which
    we then read back as numpy so it plugs into gradio's preview directly.
    """
    from modules.irodori_bridge import get_bridge
    from modules.lora_pipeline import gpu_session
    bridge = get_bridge()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        out_path = tmp.name
    try:
        with gpu_session():
            bridge.synthesize(
                mode="clone",
                text=text,
                caption=caption,
                ref_wav=ref_wav,
                out_path=out_path,
                seed=seed,
                lora_path=lora_path,
            )
        audio, sr = sf.read(out_path, dtype="float32")
        return sr, audio
    finally:
        try:
            os.remove(out_path)
        except OSError:
            pass


def save_voice(audio_tuple, name: str, sample_text: str = "") -> str:
    """Save a Voice Design generation under ``output/voice_design/``."""
    return _save_named_clip(audio_tuple, name, sample_text, VOICE_DESIGN_DIR, "voice_design")


def save_irodori_infer(audio_tuple, name: str, sample_text: str = "") -> str:
    """Save an Irodori Inference one-shot generation under ``output/irodori_infer/``."""
    from config import OUTPUT_DIR
    target_dir = OUTPUT_DIR / "irodori_infer"
    return _save_named_clip(audio_tuple, name, sample_text, target_dir, "irodori_infer")


def _save_named_clip(audio_tuple, name: str, sample_text: str, target_dir: Path, default: str) -> str:
    sr, audio = audio_tuple
    os.makedirs(target_dir, exist_ok=True)
    safe_name = _sanitize_filename(name, default=default)
    dest = str(target_dir / f"{safe_name}.wav")
    if os.path.exists(dest):
        base, ext = os.path.splitext(dest)
        i = 1
        while os.path.exists(f"{base}_{i}{ext}"):
            i += 1
        dest = f"{base}_{i}{ext}"
    sf.write(dest, audio, sr, subtype="PCM_16")
    txt_path = os.path.splitext(dest)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(sample_text)
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
