"""Download Tesseract for Windows and run PyInstaller. Intended for the Windows CI job.

Assumes a Tesseract-OCR/ directory (tesseract.exe + tessdata) is present next to this
script. CI downloads/extracts it before calling this driver.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    tess = HERE / "Tesseract-OCR" / "tesseract.exe"
    if not tess.exists():
        sys.exit(
            "Tesseract-OCR/tesseract.exe not found next to build_exe.py. "
            "CI must place the portable Tesseract there first."
        )
    subprocess.check_call(
        [sys.executable, "-m", "PyInstaller", "--onefile", "--noconfirm",
         str(HERE / "hex2ascii.spec")],
        cwd=str(HERE),
    )
    print("Built dist/Hex2ASCII.exe")


if __name__ == "__main__":
    main()
