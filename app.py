"""VoiceDesignCloner — Qwen3-TTS GUI Tool."""

import os
import sys
import io
import warnings
import logging

import asyncio
import gradio as gr
from modules.model_manager import ModelManager
from lang import t
from ui.tab_voice_design import build_voice_design_tab
from ui.tab_voice_clone import build_voice_clone_tab
from ui.tab_lora import build_lora_tab
from ui.tab_irodori_infer import build_irodori_infer_tab
from ui.tab_tools import build_tools_tab
from ui.tab_manual import build_manual_tab
from ui.tab_settings import build_settings_tab

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# Windows CJK encoding fix + suppress harmless ConnectionResetError tracebacks
_SUPPRESS_PATTERNS = (
    "ConnectionResetError",
    "WinError 10054",
    "_call_connection_lost",
)


class _FilteredStderr(io.TextIOWrapper):
    def __init__(self, buffer):
        super().__init__(buffer, encoding="utf-8", errors="replace")
        self._skip = False

    def write(self, s):
        if any(p in s for p in _SUPPRESS_PATTERNS):
            self._skip = True
        if self._skip:
            if s.strip() == "" or s == "\n":
                self._skip = False
            return len(s)
        return super().write(s)


if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "buffer"):
    sys.stderr = _FilteredStderr(sys.stderr.buffer)

# Suppress known harmless warnings
warnings.filterwarnings("ignore", message="Trying to convert audio automatically")


def _asyncio_exception_handler(loop, context):
    exc = context.get("exception")
    if isinstance(exc, ConnectionResetError):
        return
    loop.default_exception_handler(context)


try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
loop.set_exception_handler(_asyncio_exception_handler)

manager = ModelManager()
logger.info("VoiceDesignCloner starting (backend=%s)", manager.backend)

with gr.Blocks(title="VoiceDesignCloner", theme="NoCrypt/miku") as demo:
    gr.Markdown("# VoiceDesignCloner")

    with gr.Tabs():
        with gr.Tab(t("tab_voice_design")):
            build_voice_design_tab(manager)
        with gr.Tab(t("tab_voice_clone")):
            build_voice_clone_tab(manager)
        with gr.Tab(t("tab_lora")):
            build_lora_tab(manager)
        with gr.Tab(t("tab_irodori_infer")):
            build_irodori_infer_tab(manager)
        with gr.Tab(t("tab_tools")):
            build_tools_tab()
        with gr.Tab(t("tab_settings")):
            build_settings_tab(manager)
        with gr.Tab(t("tab_manual")):
            build_manual_tab()

demo.queue(default_concurrency_limit=1)
demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    inbrowser=os.environ.get("VDC_RESTART") != "1",
    share=False,
)
