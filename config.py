"""Global configuration."""

from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
VOICE_DESIGN_DIR = OUTPUT_DIR / "voice_design"
VOICE_CLONE_DIR = OUTPUT_DIR / "voice_clone"
PRESETS_DIR = BASE_DIR / "presets"
CORPUS_DIR = BASE_DIR / "corpus"

# Defaults
DEFAULT_SAMPLE_TEXT = "こんにちは、はじめまして。私の声はいかがですか？"
DEFAULT_TARGET_SR = 44100
DEFAULT_MODEL = "1.7B-Base"
DEFAULT_VOICE_DESIGN_MODEL = "1.7B-VoiceDesign"
