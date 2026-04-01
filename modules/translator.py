"""Translation module: Japanese -> Chinese/English via M2M-100."""

import threading


class Translator:
    MODEL_NAME = "facebook/m2m100_418M"

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._lock = threading.Lock()

    def preload(self):
        """Background preload so first translation doesn't block UI."""
        threading.Thread(target=self._load_model, daemon=True).start()

    def _load_model(self):
        with self._lock:
            if self.model is not None:
                return
            from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
            self.tokenizer = M2M100Tokenizer.from_pretrained(self.MODEL_NAME)
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = M2M100ForConditionalGeneration.from_pretrained(
                self.MODEL_NAME, low_cpu_mem_usage=False
            ).to(device)

    @staticmethod
    def _guess_lang(text: str) -> str:
        """Guess source language: 'ja', 'zh', or 'en'."""
        for ch in text:
            cp = ord(ch)
            if 0x3040 <= cp <= 0x309F or 0x30A0 <= cp <= 0x30FF:
                return "ja"
        # No kana found — check if mostly ASCII (English) or CJK (Chinese)
        ascii_count = sum(1 for ch in text if ch.isascii() and ch.isalpha())
        if ascii_count > len(text) * 0.3:
            return "en"
        return "zh"

    def translate(self, text: str, target_lang: str) -> str:
        """Translate text to target_lang ('zh' or 'en'). Auto-detects source."""
        if not text.strip():
            return ""
        self._load_model()  # waits for preload if still running
        src = self._guess_lang(text)
        if src == target_lang:
            return text
        self.tokenizer.src_lang = src
        inputs = self.tokenizer(text, return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        tokens = self.model.generate(
            **inputs,
            forced_bos_token_id=self.tokenizer.get_lang_id(target_lang),
            max_length=256,
        )
        return self.tokenizer.batch_decode(tokens, skip_special_tokens=True)[0]
