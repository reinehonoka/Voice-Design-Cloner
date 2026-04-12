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
_SUPPORTED_LANGS = {"ja", "en", "zh"}

def _load_lang() -> str:
    try:
        data = json.loads(_CONFIG_JSON.read_text(encoding="utf-8"))
        lang = data.get("language", "ja")
        return lang if lang in _SUPPORTED_LANGS else "ja"
    except Exception:
        return "ja"

def save_lang(lang: str) -> None:
    data = {"language": lang}
    _CONFIG_JSON.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

LANG: str = _load_lang()

# Defaults
_SAMPLE_TEXTS = {
    "ja": "こんにちは、はじめまして。私の声はいかがですか？",
    "en": "Hello, nice to meet you. How do you like my voice?",
    "zh": "你好，很高兴认识你。你觉得我的声音怎么样？",
}
DEFAULT_SAMPLE_TEXT = _SAMPLE_TEXTS.get(LANG, _SAMPLE_TEXTS["ja"])
DEFAULT_TARGET_SR = 44100
DEFAULT_MODEL = "1.7B-Base"
DEFAULT_VOICE_DESIGN_MODEL = "1.7B-VoiceDesign"
