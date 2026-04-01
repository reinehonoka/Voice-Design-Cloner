"""Utilities: preset loading, corpus loading, formatting."""

import json
import logging
from config import PRESETS_DIR, CORPUS_DIR

logger = logging.getLogger(__name__)


def load_presets(lang: str = "zh") -> dict:
    path = PRESETS_DIR / f"voice_presets_{lang}.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("Preset JSON must be an object")
        return data
    except Exception:
        logger.exception("Failed to load presets: %s", path)
        raise


def load_corpus(corpus_name: str) -> list[str]:
    path = CORPUS_DIR / corpus_name
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines
    except Exception:
        logger.exception("Failed to load corpus: %s", path)
        raise


def list_corpus_files() -> list[str]:
    return sorted(p.name for p in CORPUS_DIR.glob("*.txt"))


def format_duration(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h}h {m}m {s}s"
    if m > 0:
        return f"{m}m {s}s"
    return f"{s}s"
