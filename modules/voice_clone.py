"""VoiceClone: batch synthesis using a reference voice."""

import os
import time
import logging
import librosa
import re
import soundfile as sf
from config import OUTPUT_DIR

_TTS_LANG_MAP = {"ja": "japanese", "en": "english", "zh": "chinese"}

logger = logging.getLogger(__name__)
_SAFE_SEGMENT_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def _sanitize_segment(value: str, default: str) -> str:
    """Sanitize untrusted folder/file segments for safe relative-path use."""
    segment = (value or "").strip().replace("\\", "/")
    segment = segment.split("/")[-1]  # basename only
    segment = _SAFE_SEGMENT_RE.sub("_", segment).strip("._")
    return segment or default


def batch_clone(
    manager,
    ref_audio: str,
    ref_text: str,
    texts: list[str],
    output_folder: str = "clone",
    wavs_folder: str = "raw",
    esd_filename: str = "Neutral.txt",
    model_key: str = "1.7B-Base",
    target_sr: int = 44100,
    corpus_lang: str = "ja",
):
    """Clone a voice across all texts. Yields (progress_pct, status_msg) per file,
    then yields (1.0, stats_dict) as the final item."""
    if not ref_audio or not os.path.exists(ref_audio):
        raise FileNotFoundError(f"Reference audio not found: {ref_audio}")
    if not ref_text or not ref_text.strip():
        raise ValueError("Reference transcript is empty")
    if not texts:
        raise ValueError("No target texts were provided")

    logger.info(
        "Starting batch clone: model=%s texts=%d output_folder=%s",
        model_key, len(texts), output_folder,
    )
    manager.load_model(model_key)

    # Pre-compute reference voice features (critical optimization)
    prompt_items = manager.create_voice_clone_prompt(
        ref_audio=ref_audio,
        ref_text=ref_text,
        x_vector_only_mode=False,
    )

    safe_output_folder = _sanitize_segment(output_folder, "clone")
    safe_wavs_folder = _sanitize_segment(wavs_folder, "raw")
    safe_esd_filename = _sanitize_segment(esd_filename, "Neutral.txt")
    if not safe_esd_filename.endswith(".txt"):
        safe_esd_filename += ".txt"

    base_dir = OUTPUT_DIR / safe_output_folder
    wav_dir = str(base_dir / safe_wavs_folder)
    os.makedirs(wav_dir, exist_ok=True)

    esd_lines = []
    total = len(texts)
    total_duration = 0.0
    start_time = time.time()

    for i, text in enumerate(texts):
        if not text or not text.strip():
            logger.warning("Skipping empty text at index=%d", i)
            continue
        filename = f"{i + 1:04d}.wav"

        try:
            wavs, sr = manager.current_model.generate_voice_clone(
                text=text,
                language=_TTS_LANG_MAP.get(corpus_lang, "auto"),
                voice_clone_prompt=prompt_items,
            )
        except Exception as e:
            raise RuntimeError(f"Voice clone failed at line {i + 1}: {e}") from e

        audio = wavs[0]
        if sr != target_sr:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
        wav_path = os.path.join(wav_dir, filename)
        sf.write(wav_path, audio, target_sr, subtype="PCM_16")

        stem = os.path.splitext(filename)[0]  # "0001"
        esd_lines.append(f"{stem}|{text}")

        duration = len(wavs[0]) / sr
        total_duration += duration

        elapsed = time.time() - start_time
        avg = elapsed / (i + 1)
        remaining = avg * (total - i - 1)
        yield (i + 1) / total, f"{i + 1}/{total} | ~{remaining:.0f}s left"

    # Write text list (esd.list / Neutral.txt)
    esd_path = str(base_dir / safe_esd_filename)
    with open(esd_path, "w", encoding="utf-8") as f:
        f.write("\n".join(esd_lines))

    logger.info("Batch clone completed: generated=%d output=%s", len(esd_lines), wav_dir)
    yield 1.0, {
        "total_files": len(esd_lines),
        "total_duration_sec": total_duration,
        "output_dir": wav_dir,
        "esd_path": esd_path,
    }
