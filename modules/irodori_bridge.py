"""Bridge between vdc and the Irodori-TTS worker subprocess.

Irodori cannot share a Python process with the rest of vdc (it needs a different
torch / sentencepiece). We launch ``modules/irodori_worker.py`` inside Irodori's
own venv as a persistent subprocess and exchange newline-delimited JSON on
stdin/stdout.

Public surface:

    IrodoriBridge.is_available()   -> bool
    IrodoriBridge.ensure_started() -> None
    IrodoriBridge.synthesize(...)  -> dict      (synchronous, one-shot)
    IrodoriBridge.shutdown()       -> None
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _default_irodori_root() -> Path:
    """Return the directory where setup.bat / setup.sh installed Irodori-TTS."""
    if sys.platform == "win32":
        base = Path(os.environ.get("USERPROFILE", str(Path.home())))
    else:
        base = Path.home()
    return base / ".vdc-engines" / "Irodori-TTS"


def _worker_script_path() -> Path:
    return Path(__file__).resolve().parent / "irodori_worker.py"


class IrodoriUnavailable(RuntimeError):
    pass


class IrodoriBridge:
    """Manages a persistent Irodori worker subprocess."""

    def __init__(self, irodori_root: Path | None = None) -> None:
        self.irodori_root = irodori_root or _default_irodori_root()
        self._proc: subprocess.Popen | None = None
        self._lock = threading.Lock()
        self._stderr_buf: list[str] = []
        self._stderr_thread: threading.Thread | None = None

    # ------------------------------------------------------------------ availability

    def is_available(self) -> bool:
        """True iff Irodori was installed by setup and looks runnable."""
        py = self._worker_python()
        return self.irodori_root.is_dir() and py.is_file() and _worker_script_path().is_file()

    def _worker_python(self) -> Path:
        if sys.platform == "win32":
            return self.irodori_root / ".venv" / "Scripts" / "python.exe"
        return self.irodori_root / ".venv" / "bin" / "python"

    def status_text(self) -> str:
        if self._proc is not None and self._proc.poll() is None:
            return "running"
        if self.is_available():
            return "ready (not started)"
        return "not installed"

    # ------------------------------------------------------------------ lifecycle

    def ensure_started(self) -> None:
        with self._lock:
            if self._proc is not None and self._proc.poll() is None:
                return
            if not self.is_available():
                raise IrodoriUnavailable(
                    f"Irodori-TTS is not installed at {self.irodori_root}. "
                    "Re-run setup.bat / setup.sh."
                )
            py = self._worker_python()
            script = _worker_script_path()
            logger.info("Starting Irodori worker: %s %s (cwd=%s)", py, script, self.irodori_root)
            self._proc = subprocess.Popen(
                [str(py), str(script)],
                cwd=str(self.irodori_root),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
            self._stderr_buf = []
            self._stderr_thread = threading.Thread(
                target=self._stderr_pump, args=(self._proc.stderr,), daemon=True,
            )
            self._stderr_thread.start()
            ready = self._read_line()
            if not ready or not ready.get("ok") or ready.get("event") != "ready":
                err = self._collected_stderr()
                self._proc = None
                raise IrodoriUnavailable(f"Irodori worker did not start cleanly: {ready!r} stderr={err!r}")

    def shutdown(self) -> None:
        with self._lock:
            if self._proc is None:
                return
            try:
                if self._proc.poll() is None:
                    try:
                        self._proc.stdin.write(json.dumps({"op": "shutdown"}) + "\n")
                        self._proc.stdin.flush()
                    except Exception:
                        pass
                    try:
                        self._proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self._proc.kill()
            finally:
                self._proc = None

    # ------------------------------------------------------------------ I/O

    def _read_line(self) -> dict[str, Any] | None:
        if self._proc is None or self._proc.stdout is None:
            return None
        raw = self._proc.stdout.readline()
        if not raw:
            return None
        raw = raw.strip()
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.warning("invalid worker output: %r (%s)", raw, exc)
            return None

    def _stderr_pump(self, stream) -> None:
        try:
            for line in stream:
                self._stderr_buf.append(line)
                logger.warning("[irodori_worker] %s", line.rstrip())
        except Exception:
            pass

    def _collected_stderr(self) -> str:
        return "".join(self._stderr_buf[-200:])

    def _send(self, payload: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            if self._proc is None or self._proc.poll() is not None:
                raise IrodoriUnavailable("Irodori worker is not running")
            self._proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
            self._proc.stdin.flush()
            resp = self._read_line()
            if resp is None:
                err = self._collected_stderr()
                raise IrodoriUnavailable(f"Irodori worker returned no response. stderr={err!r}")
            return resp

    # ------------------------------------------------------------------ ops

    def synthesize(
        self,
        *,
        mode: str,
        text: str,
        out_path: str | Path,
        caption: str | None = None,
        ref_wav: str | Path | None = None,
        seed: int | None = None,
        target_sr: int | None = None,
    ) -> dict[str, Any]:
        """Run one synthesis. Starts worker if needed. Synchronous."""
        self.ensure_started()
        req = {
            "op": "synthesize",
            "mode": mode,
            "text": text,
            "out_path": str(out_path),
            "caption": caption,
            "seed": seed,
            "target_sr": target_sr,
        }
        if ref_wav is not None:
            req["ref_wav"] = str(ref_wav)
        resp = self._send(req)
        if not resp.get("ok"):
            msg = resp.get("error") or "Irodori worker reported failure"
            trace = resp.get("trace")
            if trace:
                logger.error("Irodori worker traceback:\n%s", trace)
            raise RuntimeError(msg)
        return resp


# A module-level singleton so the same worker survives across UI calls.
_bridge: IrodoriBridge | None = None


def get_bridge() -> IrodoriBridge:
    global _bridge
    if _bridge is None:
        _bridge = IrodoriBridge()
    return _bridge
