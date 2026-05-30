# build/hex2ascii.spec
# Bundles the CTK GUI plus a Tesseract-OCR/ directory placed next to this spec by
# build_exe.py before running PyInstaller. Written for PyInstaller 6.x: bytecode
# encryption (cipher), PYZ.zipped_data, and EXE.zipfiles were all removed in 6.0.
import os
from PyInstaller.utils.hooks import collect_data_files

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
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name="Hex2ASCII",
    debug=False, strip=False, upx=True, console=False,
)
