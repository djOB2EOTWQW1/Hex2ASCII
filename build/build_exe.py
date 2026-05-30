"""Download Tesseract for Windows and run PyInstaller. Intended for the Windows CI job.

Assumes a Tesseract-OCR/ directory (tesseract.exe + tessdata) is present next to this
script. CI downloads/extracts it before calling this driver.
"""

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TESS_DIR = HERE / "Tesseract-OCR"


def _normalize_tesseract() -> Path:
    """Ensure ``build/Tesseract-OCR/tesseract.exe`` exists.

    The UB-Mannheim installer, when extracted with 7-Zip, can nest tesseract.exe and
    tessdata/ in a subdirectory. Locate tesseract.exe anywhere under build/ and, if it
    is not already at the expected root, flatten its containing directory up to
    ``build/Tesseract-OCR/`` so the PyInstaller spec and runtime path resolution work.
    """
    expected = TESS_DIR / "tesseract.exe"
    if expected.exists():
        return expected
    matches = list(HERE.rglob("tesseract.exe"))
    if not matches:
        sys.exit(
            "tesseract.exe not found under build/. "
            "CI must download and extract the portable Tesseract first."
        )
    src_root = matches[0].parent
    TESS_DIR.mkdir(parents=True, exist_ok=True)
    for item in src_root.iterdir():
        dest = TESS_DIR / item.name
        if dest.resolve() == item.resolve():
            continue
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)
    if not expected.exists():
        sys.exit(f"Failed to normalize Tesseract layout into {TESS_DIR}.")
    return expected


def main():
    _normalize_tesseract()
    # NOTE: do not pass --onefile here. When a .spec file is given, PyInstaller
    # rejects makespec-only options like --onefile; onefile mode is already defined
    # by the EXE()/lack of COLLECT() in hex2ascii.spec.
    subprocess.check_call(
        [sys.executable, "-m", "PyInstaller", "--noconfirm",
         str(HERE / "hex2ascii.spec")],
        cwd=str(HERE),
    )
    print("Built dist/Hex2ASCII.exe")


if __name__ == "__main__":
    main()
