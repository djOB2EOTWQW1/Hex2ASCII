# build/hex2ascii.spec
# Bundles the CTK GUI plus a Tesseract-OCR/ directory placed next to this spec by
# build_exe.py before running PyInstaller.
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None
here = os.path.abspath(os.getcwd())

datas = collect_data_files("customtkinter")
tess_dir = os.path.join(here, "Tesseract-OCR")
if os.path.isdir(tess_dir):
    for root, _dirs, files in os.walk(tess_dir):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(root, here)
            datas.append((full, rel))

a = Analysis(
    ["../app.py"],
    pathex=[".."],
    binaries=[],
    datas=datas,
    hiddenimports=["gui_ctk.app", "core.ocr", "core.hexdecode"],
    hookspath=[],
    runtime_hooks=[],
    excludes=["PySide6"],
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name="Hex2ASCII",
    debug=False, strip=False, upx=True, console=False,
)
