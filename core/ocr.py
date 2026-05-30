"""Image preprocessing and multi-pass OCR for hex strings."""

import numpy as np
import pytesseract
from PIL import Image

from core import hexdecode, tesseract

_SCALE = 3


def _otsu_threshold(gray: np.ndarray) -> int:
    """Compute an Otsu threshold for a single-channel uint8 array."""
    hist, _ = np.histogram(gray, bins=256, range=(0, 256))
    total = gray.size
    sum_total = np.dot(np.arange(256), hist)
    sum_b = 0.0
    w_b = 0.0
    best_t, best_var = 0, 0.0
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sum_total - sum_b) / w_f
        var = w_b * w_f * (m_b - m_f) ** 2
        if var > best_var:
            best_var, best_t = var, t
    return best_t


def preprocess(img: Image.Image) -> list[Image.Image]:
    """Return candidate images for OCR: grayscale, upscaled, binarized, and inverted."""
    gray = img.convert("L").resize(
        (img.width * _SCALE, img.height * _SCALE), Image.LANCZOS
    )
    arr = np.asarray(gray, dtype=np.uint8)
    t = _otsu_threshold(arr)
    binary = (arr > t).astype(np.uint8) * 255

    if binary.mean() < 127:
        binary = 255 - binary

    bin_img = Image.fromarray(binary, mode="L")
    inverted = Image.fromarray(255 - binary, mode="L")
    return [bin_img, inverted, gray]


_PSM_MODES = (6, 7, 11, 4)
_WHITELIST = "0123456789abcdefABCDEFxX "


def run_ocr(img: Image.Image, psm: int) -> str:
    """Single OCR pass with a fixed PSM, LSTM engine, and hex whitelist."""
    config = (
        f"--oem 1 --psm {psm} "
        f"-c tessedit_char_whitelist={_WHITELIST}"
    )
    return pytesseract.image_to_string(img, config=config)


def best_extraction(img: Image.Image) -> str:
    """Run OCR over every (preprocessed image x PSM) and return the highest-scoring
    raw text."""
    tesseract.configure()
    best_text, best_score = "", -1.0
    for variant in preprocess(img):
        for psm in _PSM_MODES:
            try:
                text = run_ocr(variant, psm)
            except pytesseract.TesseractError:
                continue
            s = hexdecode.score(text)
            if s > best_score:
                best_score, best_text = s, text
    return best_text
