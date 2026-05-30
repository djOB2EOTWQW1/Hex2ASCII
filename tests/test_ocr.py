from PIL import Image
from core.ocr import preprocess

def test_preprocess_returns_grayscale_images():
    img = Image.new("RGB", (40, 20), (255, 255, 255))
    variants = preprocess(img)
    assert len(variants) >= 1
    for v in variants:
        assert v.mode in ("L", "1")
        assert v.width >= img.width * 2


import shutil
import pytest
from PIL import Image, ImageDraw, ImageFont
from core.ocr import best_extraction

needs_tesseract = pytest.mark.skipif(
    shutil.which("tesseract") is None, reason="tesseract not installed"
)

@needs_tesseract
def test_best_extraction_recovers_known_hex():
    img = Image.new("RGB", (320, 80), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSansMono.ttf", 36)
    except OSError:
        font = ImageFont.load_default()
    draw.text((10, 20), "48 65 6c 6c 6f", fill="black", font=font)
    raw = best_extraction(img)
    from core.hexdecode import decode_text
    assert decode_text(raw) == "Hello"
