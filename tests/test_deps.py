from core.deps import format_missing_message, detect_package_manager, PACKAGE_NAMES

def test_format_missing_message_is_english_and_lists_packages():
    msg = format_missing_message(["tesseract", "PySide6"], manager="pacman")
    assert "Missing required packages" in msg
    assert "Install" in msg
    assert "sudo pacman -S" in msg
    assert PACKAGE_NAMES["pacman"]["tesseract"] in msg
    assert PACKAGE_NAMES["pacman"]["PySide6"] in msg

def test_format_missing_message_apt():
    msg = format_missing_message(["tesseract"], manager="apt")
    assert "sudo apt install" in msg
    assert "tesseract-ocr" in msg

def test_detect_package_manager_returns_known(monkeypatch):
    monkeypatch.setattr("core.deps._os_release_id", lambda: "arch")
    assert detect_package_manager() == "pacman"
