"""Linux PySide6 frontend for Hex2ASCII."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QFrame, QHBoxLayout, QLabel, QMessageBox,
    QPushButton, QTextEdit, QVBoxLayout, QWidget,
)

from core import clipboard, deps, ocr
from core.hexdecode import decode_text
from gui_qt.theme import ThemeWatcher


class Hex2AsciiWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hex2ASCII")
        self.resize(720, 560)

        self.theme = ThemeWatcher(self)
        self.theme.changed.connect(self.setStyleSheet)
        self.setStyleSheet(self.theme.current_qss())

        title = QLabel("Hex2ASCII")
        title.setObjectName("title")

        self.preview = QLabel("Drop or load an image of a hex string")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(180)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.addWidget(self.preview)

        clip_btn = QPushButton("Process clipboard")
        clip_btn.clicked.connect(self.process_clipboard)
        file_btn = QPushButton("Open image…")
        file_btn.clicked.connect(self.process_file)
        copy_btn = QPushButton("Copy result")
        copy_btn.clicked.connect(self.copy_result)

        buttons = QHBoxLayout()
        buttons.addWidget(clip_btn)
        buttons.addWidget(file_btn)
        buttons.addWidget(copy_btn)

        self.result = QTextEdit()
        self.result.setReadOnly(False)
        self.result.setPlaceholderText("Decoded ASCII appears here")

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(card)
        layout.addLayout(buttons)
        layout.addWidget(self.result)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event):
        md = event.mimeData()
        if md.hasUrls():
            self._decode_path(md.urls()[0].toLocalFile())

    def process_clipboard(self):
        img = clipboard.grab_image()
        if img is None:
            QMessageBox.critical(self, "Error", "No image in the clipboard.")
            return
        self._show_preview_from_image(img)
        self._decode_image(img)

    def process_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if path:
            self._decode_path(path)

    def _decode_path(self, path: str):
        from PIL import Image
        try:
            img = Image.open(path)
        except OSError as exc:
            QMessageBox.critical(self, "Error", f"Cannot open file: {exc}")
            return
        self.preview.setPixmap(
            QPixmap(path).scaledToHeight(180, Qt.SmoothTransformation)
        )
        self._decode_image(img)

    def _show_preview_from_image(self, img):
        import io
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="PNG")
        pix = QPixmap()
        pix.loadFromData(buf.getvalue())
        self.preview.setPixmap(pix.scaledToHeight(180, Qt.SmoothTransformation))

    def _decode_image(self, img):
        raw = ocr.best_extraction(img)
        text = decode_text(raw)
        if not text:
            QMessageBox.warning(self, "No result", "No hex text found in the image.")
            return
        self.result.setPlainText(text)

    def copy_result(self):
        QApplication.clipboard().setText(self.result.toPlainText())


def main():
    missing = deps.check_dependencies()
    if missing:
        print(deps.format_missing_message(missing), file=sys.stderr)
        try:
            app = QApplication(sys.argv)
            QMessageBox.critical(None, "Missing dependencies",
                                 deps.format_missing_message(missing))
        except Exception:
            pass
        sys.exit(1)

    app = QApplication(sys.argv)
    win = Hex2AsciiWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
