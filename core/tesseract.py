"""Locate the tesseract binary: bundled on a frozen Windows build, system otherwise."""

import os
import sys
from pathlib import Path

import pytesseract


def find_tesseract() -> str:
    """Return the path/command for the tesseract binary."""
    if getattr(sys, "frozen", False):
        bundled = Path(sys._MEIPASS) / "Tesseract-OCR" / "tesseract.exe"
        if bundled.exists():
            return str(bundled)
    return "tesseract"


def configure() -> None:
    """Point pytesseract at the resolved binary."""
    pytesseract.pytesseract.tesseract_cmd = find_tesseract()
