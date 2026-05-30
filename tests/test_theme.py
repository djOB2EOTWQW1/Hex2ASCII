import json
from gui_qt.theme import load_colors, build_qss, FALLBACK_COLORS

def test_load_colors_reads_file(tmp_path):
    p = tmp_path / "colors.json"
    p.write_text(json.dumps({"surface": "#161313", "on_surface": "#e8e1e1",
                             "primary": "#ddbfc4", "on_primary": "#3e2b2f"}))
    colors = load_colors(str(p))
    assert colors["surface"] == "#161313"

def test_load_colors_falls_back_when_missing(tmp_path):
    colors = load_colors(str(tmp_path / "nope.json"))
    assert colors == FALLBACK_COLORS

def test_build_qss_uses_color_roles():
    qss = build_qss({"surface": "#161313", "on_surface": "#e8e1e1",
                     "primary": "#ddbfc4", "on_primary": "#3e2b2f",
                     "surface_container": "#221f1f", "outline": "#958f8f",
                     "error": "#ffb4ab", "surface_container_high": "#2d2929"})
    assert "#161313" in qss
    assert "#ddbfc4" in qss
