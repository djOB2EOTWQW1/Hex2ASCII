"""Runtime dependency checks and an English missing-package message for Linux."""

import importlib.util
import shutil
import subprocess
from pathlib import Path

PACKAGE_NAMES = {
    "pacman": {
        "tesseract": "tesseract",
        "eng_data": "tesseract-data-eng",
        "PySide6": "python-pyside6",
        "PIL": "python-pillow",
        "pytesseract": "python-pytesseract",
        "numpy": "python-numpy",
    },
    "apt": {
        "tesseract": "tesseract-ocr",
        "eng_data": "tesseract-ocr-eng",
        "PySide6": "python3-pyside6",
        "PIL": "python3-pil",
        "pytesseract": "python3-pytesseract",
        "numpy": "python3-numpy",
    },
    "dnf": {
        "tesseract": "tesseract",
        "eng_data": "tesseract-langpack-eng",
        "PySide6": "python3-pyside6",
        "PIL": "python3-pillow",
        "pytesseract": "python3-pytesseract",
        "numpy": "python3-numpy",
    },
}

_INSTALL_CMD = {
    "pacman": "sudo pacman -S",
    "apt": "sudo apt install",
    "dnf": "sudo dnf install",
}

_ID_TO_MANAGER = {
    "arch": "pacman", "cachyos": "pacman", "manjaro": "pacman", "endeavouros": "pacman",
    "debian": "apt", "ubuntu": "apt", "linuxmint": "apt", "pop": "apt",
    "fedora": "dnf", "rhel": "dnf", "centos": "dnf",
}

_PY_MODULES = ["PySide6", "PIL", "pytesseract", "numpy"]


def _os_release_id() -> str:
    path = Path("/etc/os-release")
    if not path.exists():
        return ""
    for line in path.read_text().splitlines():
        if line.startswith("ID="):
            return line.split("=", 1)[1].strip().strip('"')
    return ""


def detect_package_manager() -> str:
    """Return 'pacman' | 'apt' | 'dnf', best-effort, defaulting to apt."""
    mgr = _ID_TO_MANAGER.get(_os_release_id())
    if mgr:
        return mgr
    for candidate in ("pacman", "apt", "dnf"):
        if shutil.which(candidate):
            return candidate
    return "apt"


def _has_english_langdata() -> bool:
    """Return True if Tesseract reports English ('eng') training data."""
    try:
        out = subprocess.run(
            ["tesseract", "--list-langs"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    langs = out.stdout.splitlines() + out.stderr.splitlines()
    return any(line.strip() == "eng" for line in langs)


def check_dependencies() -> list[str]:
    """Return logical names of missing dependencies (empty list = all present)."""
    missing = []
    if shutil.which("tesseract") is None:
        # No binary means no language data either; report both so the user installs
        # everything in one go.
        missing.append("tesseract")
        missing.append("eng_data")
    elif not _has_english_langdata():
        missing.append("eng_data")
    for mod in _PY_MODULES:
        if importlib.util.find_spec(mod) is None:
            missing.append(mod)
    return missing


def format_missing_message(missing: list[str], manager: str | None = None) -> str:
    """English message naming missing packages and the install command."""
    manager = manager or detect_package_manager()
    names = PACKAGE_NAMES.get(manager, PACKAGE_NAMES["apt"])
    pkgs = [names.get(m, m) for m in missing]
    cmd = _INSTALL_CMD.get(manager, _INSTALL_CMD["apt"])
    return (
        "Missing required packages: " + ", ".join(pkgs) + "\n"
        "Install them with:\n    " + cmd + " " + " ".join(pkgs)
    )
