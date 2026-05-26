"""Model loading, unloading, switching, and device detection."""

import gc
import logging
import torch

logger = logging.getLogger(__name__)

BACKENDS = ["standard", "faster", "irodori"]

BACKEND_LABELS = {
    "standard": "Qwen3-TTS",
    "faster": "faster",
    "irodori": "Irodori-TTS",
}


def _faster_available() -> bool:
    """Check if faster-qwen3-tts is installed."""
    try:
        import faster_qwen3_tts  # noqa: F401
        return True
    except ImportError:
        return False


def _irodori_available() -> bool:
    """Check if Irodori-TTS has been installed by setup."""
    from modules.irodori_bridge import get_bridge
    return get_bridge().is_available()


class ModelManager:
    MODELS = {
        "1.7B-VoiceDesign": "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
        "1.7B-Base": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
        "0.6B-Base": "Qwen/Qwen3-TTS-12Hz-0.6B-Base",
    }

    CLONE_MODELS = ["1.7B-Base", "0.6B-Base"]

    def __init__(self):
        self.current_model = None
        self.current_model_name = None
        self.current_backend = None
        self.device = self._detect_device()
        self.dtype = torch.bfloat16 if self.device == "cuda" else torch.float32
        self.attn_impl = "sdpa" if self.device == "cuda" else None
        self.backend = self._initial_backend()

    @staticmethod
    def _initial_backend() -> str:
        from config import load_backend
        persisted = load_backend()
        if persisted == "irodori" and _irodori_available():
            return "irodori"
        if persisted == "faster" and _faster_available():
            return "faster"
        if persisted == "standard":
            return "standard"
        return "faster" if _faster_available() else "standard"

    def _detect_device(self):
        return "cuda" if torch.cuda.is_available() else "cpu"

    def set_backend(self, backend: str):
        """Switch backend. Forces model reload on next load_model call."""
        if backend not in BACKENDS:
            raise ValueError(f"Unknown backend: {backend}. Choose from {BACKENDS}")
        if backend == "faster" and not _faster_available():
            raise RuntimeError(
                "faster-qwen3-tts is not installed. "
                "Run: pip install faster-qwen3-tts"
            )
        if backend == "irodori" and not _irodori_available():
            raise RuntimeError(
                "Irodori-TTS is not installed. Run setup.bat / setup.sh."
            )
        if backend != self.backend:
            logger.info("Backend changed: %s -> %s", self.backend, backend)
            # Leaving the old qwen model loaded would just waste VRAM while
            # the user is on the Irodori backend, and vice versa.
            self.unload_model()
            self._shutdown_irodori_if_switching_away(backend)
            self.backend = backend

    def _shutdown_irodori_if_switching_away(self, new_backend: str) -> None:
        if self.backend == "irodori" and new_backend != "irodori":
            try:
                from modules.irodori_bridge import get_bridge
                get_bridge().shutdown()
            except Exception:
                logger.exception("Failed to shut down Irodori worker cleanly")

    def load_model(self, model_key: str):
        if self.backend == "irodori":
            # Irodori has no per-tab Qwen-style model swap; the worker chooses
            # the right checkpoint (v3 for clone, v2-VoiceDesign for design)
            # on demand.
            return
        if self.current_model_name == model_key and self.current_backend == self.backend:
            logger.debug("Model already loaded: %s (%s)", model_key, self.backend)
            return
        if model_key not in self.MODELS:
            raise ValueError(f"Unknown model key: {model_key}")
        self.unload_model()

        model_id = self.MODELS[model_key]

        # 0.6B models are known to fail CUDA graph capture in faster backend
        FASTER_UNSUPPORTED = {"0.6B-Base"}
        use_faster = self.backend == "faster" and self.device == "cuda" and model_key not in FASTER_UNSUPPORTED

        if use_faster:
            from faster_qwen3_tts import FasterQwen3TTS

            logger.info("Loading model (faster): %s (%s)", model_key, model_id)
            try:
                self.current_model = FasterQwen3TTS.from_pretrained(
                    model_id,
                    device=self.device,
                    dtype=self.dtype,
                    attn_implementation=self.attn_impl,
                )
                self.current_backend = "faster"
            except Exception as e:
                logger.warning(
                    "faster backend failed (%s), falling back to standard: %s",
                    model_key, e,
                )
                torch.cuda.empty_cache()
                gc.collect()
                from qwen_tts import Qwen3TTSModel
                self.current_model = Qwen3TTSModel.from_pretrained(
                    model_id,
                    device_map=self.device,
                    dtype=self.dtype,
                    attn_implementation=self.attn_impl,
                )
                self.current_backend = "standard"
                logger.info("Loaded model (standard fallback): %s", model_key)
        else:
            from qwen_tts import Qwen3TTSModel

            logger.info("Loading model (standard): %s (%s)", model_key, model_id)
            self.current_model = Qwen3TTSModel.from_pretrained(
                model_id,
                device_map=self.device,
                dtype=self.dtype,
                attn_implementation=self.attn_impl,
            )
            self.current_backend = "standard"

        self.current_model_name = model_key
        logger.info("Model loaded: %s (%s)", model_key, self.current_backend)

    def unload_model(self):
        if self.current_model is not None:
            logger.info("Unloading model: %s (%s)", self.current_model_name, self.current_backend)
            del self.current_model
            self.current_model = None
            self.current_model_name = None
            self.current_backend = None
            if self.device == "cuda":
                torch.cuda.empty_cache()
            gc.collect()

    def create_voice_clone_prompt(self, ref_audio, ref_text, x_vector_only_mode=False):
        """Create voice clone prompt, works with both backends."""
        if self.current_backend == "faster":
            return self.current_model.model.create_voice_clone_prompt(
                ref_audio=ref_audio,
                ref_text=ref_text,
                x_vector_only_mode=x_vector_only_mode,
            )
        else:
            return self.current_model.create_voice_clone_prompt(
                ref_audio=ref_audio,
                ref_text=ref_text,
                x_vector_only_mode=x_vector_only_mode,
            )

    def get_vram_info(self) -> str:
        if self.device != "cuda":
            return "CPU mode"
        allocated = torch.cuda.memory_allocated() / 1024**3
        total = torch.cuda.get_device_properties(0).total_memory / 1024**3
        return f"{allocated:.1f} GB / {total:.1f} GB"

    def get_gpu_name(self) -> str:
        if self.device != "cuda":
            return "CPU"
        return torch.cuda.get_device_name(0)
