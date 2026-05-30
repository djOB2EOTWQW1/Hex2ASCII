"""OCR-text correction, hex extraction, byte decoding, and candidate scoring."""

import re
from dataclasses import dataclass

_CONFUSION = {
    "O": "0", "o": "0",
    "l": "1", "I": "1", "i": "1",
    "S": "5", "s": "5",
    "Z": "2", "z": "2",
    "G": "6", "g": "6",
    "Q": "0",
}
_HEX_LETTERS = set("abcdefABCDEF")


def correct_ocr(text: str) -> str:
    """Replace common OCR lookalike letters with digits, but never touch valid hex
    letters (A-F)."""
    out = []
    for ch in text:
        if ch in _HEX_LETTERS:
            out.append(ch)
        else:
            out.append(_CONFUSION.get(ch, ch))
    return "".join(out)
