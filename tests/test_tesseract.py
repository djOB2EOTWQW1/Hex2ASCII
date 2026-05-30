import sys
from core.tesseract import find_tesseract

def test_find_tesseract_returns_system_when_not_frozen(monkeypatch):
    monkeypatch.delattr(sys, "frozen", raising=False)
    assert find_tesseract() == "tesseract"
