"""Cross-platform clipboard image grab."""

import io
import shutil
import subprocess

from PIL import Image, ImageGrab


def _grab_wayland():
    """Try wl-paste (Wayland). Returns a PIL image or None."""
    if shutil.which("wl-paste") is None:
        return None
    try:
        data = subprocess.run(
            ["wl-paste", "--type", "image/png"],
            capture_output=True, timeout=5,
        ).stdout
    except (subprocess.SubprocessError, OSError):
        return None
    if not data:
        return None
    try:
        return Image.open(io.BytesIO(data))
    except OSError:
        return None


def grab_image():
    """Return a PIL.Image from the clipboard, or None if there is no image."""
    try:
        img = ImageGrab.grabclipboard()
    except Exception:
        img = None
    if isinstance(img, Image.Image):
        return img
    return _grab_wayland()
