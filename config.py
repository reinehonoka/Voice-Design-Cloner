"""Global configuration."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
VOICE_DESIGN_DIR = OUTPUT_DIR / "voice_design"
VOICE_CLONE_DIR = OUTPUT_DIR / "voice_clone"
PRESETS_DIR = BASE_DIR / "presets"
CORPUS_DIR = BASE_DIR / "corpus"

# Language setting
_CONFIG_JSON = BASE_DIR / "config.json"
_SUPPORTED_LANGS = {"ja", "en", "zh", "ko"}

def _load_config() -> dict:
    try:
        return json.loads(_CONFIG_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_config(data: dict) -> None:
    _CONFIG_JSON.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _load_lang() -> str:
    data = _load_config()
    lang = data.get("language", "ja")
    return lang if lang in _SUPPORTED_LANGS else "ja"


def save_lang(lang: str) -> None:
    data = _load_config()
    data["language"] = lang
    _save_config(data)


def load_backend() -> str | None:
    """Return the persisted backend key, or None if not set."""
    return _load_config().get("backend")


def save_backend(backend: str) -> None:
    data = _load_config()
    data["backend"] = backend
    _save_config(data)

LANG: str = _load_lang()

# Mapping from UI language code to Qwen3-TTS language parameter
_TTS_LANG_MAP = {
    "ja": "japanese",
    "en": "english",
    "zh": "chinese",
    "ko": "korean",
}
TTS_LANG: str = _TTS_LANG_MAP.get(LANG, "auto")

# Defaults
_SAMPLE_TEXTS = {
    "ja": "こんにちは、はじめまして。私の声はいかがですか？",
    "en": "Hello, nice to meet you. How do you like my voice?",
    "zh": "你好，很高兴认识你。你觉得我的声音怎么样？",
    "ko": "안녕하세요, 처음 뵙겠습니다. 제 목소리는 어떠세요?",
}
DEFAULT_SAMPLE_TEXT = _SAMPLE_TEXTS.get(LANG, _SAMPLE_TEXTS["ja"])
DEFAULT_TARGET_SR = 44100
DEFAULT_MODEL = "1.7B-Base"
DEFAULT_VOICE_DESIGN_MODEL = "1.7B-VoiceDesign"
