from PIL import Image
from core.ocr import preprocess

def test_preprocess_returns_grayscale_images():
    img = Image.new("RGB", (40, 20), (255, 255, 255))
    variants = preprocess(img)
    assert len(variants) >= 1
    for v in variants:
        assert v.mode in ("L", "1")
        assert v.width >= img.width * 2
