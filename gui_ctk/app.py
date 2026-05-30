"""Windows CustomTkinter frontend for Hex2ASCII."""

import customtkinter as ctk
from tkinter import filedialog, messagebox

from PIL import Image

from core import clipboard, ocr
from core.hexdecode import decode_text

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hex2ASCII")
        self.geometry("640x560")

        ctk.CTkLabel(self, text="Hex2ASCII",
                     font=("Segoe UI", 22, "bold")).pack(pady=(16, 8))

        self.preview = ctk.CTkLabel(self, text="Load an image of a hex string",
                                    height=160)
        self.preview.pack(pady=8, padx=16, fill="x")

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=8)
        ctk.CTkButton(row, text="Process clipboard", corner_radius=12,
                      command=self.process_clipboard).pack(side="left", padx=6)
        ctk.CTkButton(row, text="Open image…", corner_radius=12,
                      command=self.process_file).pack(side="left", padx=6)
        ctk.CTkButton(row, text="Copy result", corner_radius=12,
                      command=self.copy_result).pack(side="left", padx=6)

        self.result = ctk.CTkTextbox(self, height=220, corner_radius=12)
        self.result.pack(pady=8, padx=16, fill="both", expand=True)

    def process_clipboard(self):
        img = clipboard.grab_image()
        if img is None:
            messagebox.showerror("Error", "No image in the clipboard.")
            return
        self._decode(img)

    def process_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if not path:
            return
        try:
            img = Image.open(path)
        except OSError as exc:
            messagebox.showerror("Error", f"Cannot open file: {exc}")
            return
        self._show_preview(img)
        self._decode(img)

    def _show_preview(self, img):
        thumb = img.convert("RGB").copy()
        thumb.thumbnail((360, 160))
        ctk_img = ctk.CTkImage(light_image=thumb, dark_image=thumb, size=thumb.size)
        self.preview.configure(image=ctk_img, text="")
        self.preview.image = ctk_img

    def _decode(self, img):
        raw = ocr.best_extraction(img)
        text = decode_text(raw)
        if not text:
            messagebox.showwarning("No result", "No hex text found in the image.")
            return
        self.result.delete("1.0", "end")
        self.result.insert("end", text)

    def copy_result(self):
        text = self.result.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)


def main():
    from core import tesseract
    tesseract.configure()
    App().mainloop()


if __name__ == "__main__":
    main()
