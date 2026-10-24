"""Optional voice input via faster-whisper.

The package is NOT required. If it is missing, the endpoint returns a clear
JSON error and the UI hides the microphone.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

_model = None
_load_error: Optional[str] = None


class WhisperUnavailable(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def _get_model():
    global _model, _load_error
    if _load_error:
        raise WhisperUnavailable(_load_error)
    if _model is not None:
        return _model
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        _load_error = (
            "faster-whisper is not installed. "
            "Voice input is optional. Install with: pip install faster-whisper"
        )
        raise WhisperUnavailable(_load_error)
    try:
        model_name = os.getenv("WHISPER_MODEL", "small")
        _model = WhisperModel(model_name, device="cpu", compute_type="int8")
    except Exception as exc:
        try:
            _model = WhisperModel("base", device="cpu", compute_type="int8")
        except Exception:
            _load_error = f"Could not load Whisper model: {exc}"
            raise WhisperUnavailable(_load_error)
    return _model


def transcribe_file(path: Path, language: Optional[str] = None) -> str:
    """Transcribe an audio file to text. Raises WhisperUnavailable on failure."""
    model = _get_model()
    lang = None
    if language:
        code = language.strip().lower()[:2]
        if code in {"hi", "mr", "pa", "gu", "ta", "te", "en"}:
            lang = code
    segments, _info = model.transcribe(str(path), language=lang)
    parts = [seg.text.strip() for seg in segments if seg.text and seg.text.strip()]
    return " ".join(parts).strip()
