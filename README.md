# Hex2ASCII

Hex2ASCII reads an image of a hexadecimal string and decodes it to ASCII text
using Tesseract OCR. On Linux the app uses a PySide6 (Qt) interface with
Material You theming; on Windows it uses a CustomTkinter interface with
Tesseract bundled in the executable. Both backends share the same multi-pass
OCR engine that tries multiple image pre-processing variants and Tesseract PSM
modes to maximise recognition accuracy.

---

## Install

Download the artifact for your platform from the
[GitHub Releases](../../releases) page.

### Windows

Download **`Hex2ASCII.exe`** — Tesseract is bundled inside; no separate
install is needed. Double-click to run.

### Arch Linux / CachyOS / Manjaro

```
sudo pacman -U hex2ascii-*.pkg.tar.zst
```

### Debian / Ubuntu

```
sudo apt install ./hex2ascii_2.0.0_all.deb
```

### Generic Linux (AppImage)

```
chmod +x Hex2ASCII-x86_64.AppImage
./Hex2ASCII-x86_64.AppImage
```

---

## Linux system requirements

The Linux builds depend on **system packages**, not bundled libraries. Install
them before running:

| Dependency | Arch / CachyOS | Debian / Ubuntu |
|---|---|---|
| Tesseract OCR binary | `tesseract` | `tesseract-ocr` |
| PySide6 (Qt bindings) | `python-pyside6` | `python3-pyside6` |
| Pillow | `python-pillow` | `python3-pil` |
| numpy | `python-numpy` | `python3-numpy` |
| pytesseract | `python-pytesseract` | `python3-pytesseract` |

If any dependency is missing, the app prints an English message to stderr that
lists exactly which packages to install and the command to run — for example:

```
Missing required packages: tesseract, python-pyside6
Install them with:
    sudo pacman -S tesseract python-pyside6
```

---

## Theming (Linux)

The Qt frontend reads Material You colors from:

```
~/.local/state/quickshell/user/generated/colors.json
```

This path is the output location used by
[matugen](https://github.com/InioX/matugen) /
[illogical-impulse](https://github.com/end-4/dots-hyprland). When that file
changes on disk the app recolors itself live without restarting.

Override the path with the `HEX2ASCII_COLORS` environment variable:

```
HEX2ASCII_COLORS=/path/to/my-colors.json python app.py
```

If the file is absent or unreadable the app falls back to a built-in dark
theme automatically.

---

## Run from source

```bash
pip install -r requirements-linux.txt   # Linux
# or
pip install -r requirements-win.txt     # Windows

python app.py
```

Pass `--backend qt` or `--backend ctk` to force a specific GUI backend
(default: `qt` on Linux, `ctk` on Windows).

---

## Build from source

All four packages are built automatically by GitHub Actions when a `v*` tag is
pushed. To build locally:

| Target | Command |
|---|---|
| AppImage (Linux) | `bash build/build_appimage.sh` |
| Arch package | `cd build && makepkg` (uses `build/PKGBUILD`) |
| Debian package | `bash build/build_deb.sh` |
| Windows EXE | `python build/build_exe.py` (run on Windows) |

---

## Usage

1. Take a screenshot of a hexadecimal string to your clipboard, or have an
   image file ready.
2. Click **"Process clipboard"** to decode the clipboard image, or click
   **"Open image…"** to pick a file from disk.
3. The decoded ASCII text appears in the result box.
4. Click **"Copy result"** to copy it to the clipboard.

The OCR engine runs multiple pre-processing passes (grayscale upscale, Otsu
binarisation, inversion) combined with several Tesseract PSM modes and picks
the candidate that scores highest as a valid hex string.
