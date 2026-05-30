"""Load matugen Material You colors and turn them into a Qt stylesheet."""

import json
import os
from pathlib import Path

DEFAULT_COLORS_PATH = os.path.expanduser(
    "~/.local/state/quickshell/user/generated/colors.json"
)

FALLBACK_COLORS = {
    "background": "#161313",
    "surface": "#161313",
    "surface_container": "#221f1f",
    "surface_container_high": "#2d2929",
    "on_surface": "#e8e1e1",
    "on_surface_variant": "#ccc5c5",
    "primary": "#ddbfc4",
    "on_primary": "#3e2b2f",
    "outline": "#958f8f",
    "error": "#ffb4ab",
}


def colors_path() -> str:
    """The colors.json path, overridable via $HEX2ASCII_COLORS."""
    return os.environ.get("HEX2ASCII_COLORS", DEFAULT_COLORS_PATH)


def load_colors(path: str | None = None) -> dict:
    """Read the matugen colors JSON, or return FALLBACK_COLORS if unavailable."""
    path = path or colors_path()
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return dict(FALLBACK_COLORS)
    merged = dict(FALLBACK_COLORS)
    merged.update({k: v for k, v in data.items() if isinstance(v, str)})
    return merged


def build_qss(colors: dict) -> str:
    """Build a Qt stylesheet from Material You color roles."""
    c = dict(FALLBACK_COLORS)
    c.update(colors)
    return f"""
    QWidget {{
        background-color: {c['surface']};
        color: {c['on_surface']};
        font-family: 'Segoe UI', 'Cantarell', sans-serif;
        font-size: 14px;
    }}
    QPushButton {{
        background-color: {c['primary']};
        color: {c['on_primary']};
        border: none;
        border-radius: 12px;
        padding: 10px 18px;
        font-weight: 600;
    }}
    QPushButton:hover {{ background-color: {c['surface_container_high']}; color: {c['on_surface']}; }}
    QPushButton:disabled {{ background-color: {c['surface_container']}; color: {c['outline']}; }}
    QTextEdit, QPlainTextEdit {{
        background-color: {c['surface_container']};
        color: {c['on_surface']};
        border: 1px solid {c['outline']};
        border-radius: 12px;
        padding: 8px;
    }}
    QLabel#title {{ font-size: 20px; font-weight: 700; color: {c['primary']}; }}
    QFrame#card {{ background-color: {c['surface_container']}; border-radius: 16px; }}
    """
