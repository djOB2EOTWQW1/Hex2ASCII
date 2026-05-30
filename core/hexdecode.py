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


def extract_hex(text: str) -> str:
    """Pull a clean hex string out of arbitrary OCR text.

    Strips ``0x`` prefixes, extracts runs of hex digits that are not embedded in
    non-hex words, and drops a trailing unpaired nibble so the result always has
    an even length.
    """
    no_prefix = re.sub(r"0[xX]", "", text)
    # Extract only tokens that consist entirely of hex digits (i.e. not
    # embedded in words that contain non-hex characters like 'h', 'x', etc.)
    tokens = re.findall(r"\b[0-9a-fA-F]+\b", no_prefix)
    digits = "".join(tokens)
    if len(digits) % 2 != 0:
        digits = digits[:-1]
    return digits


@dataclass
class DecodeResult:
    text: str
    encoding: str


def decode(hex_str: str) -> DecodeResult:
    """Decode a hex string to text, trying ASCII, then UTF-8, then latin-1.

    latin-1 cannot fail, so data is never silently dropped.
    """
    if not hex_str:
        return DecodeResult(text="", encoding="ascii")
    raw = bytes.fromhex(hex_str)
    for enc in ("ascii", "utf-8", "latin-1"):
        try:
            return DecodeResult(text=raw.decode(enc), encoding=enc)
        except UnicodeDecodeError:
            continue
    return DecodeResult(text=raw.decode("latin-1", errors="replace"), encoding="latin-1")
