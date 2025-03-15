import customtkinter as ctk
from tkinter import messagebox, filedialog
from image_processor import get_image_from_clipboard, get_image_from_file, extract_hex_from_image, hex_to_ascii, copy_to_clipboard, translate_text_deeplx, start_deeplx_server
import subprocess
import sys
import os

if getattr(sys, 'frozen', False):
    deeplx_path = os.path.join(sys._MEIPASS, "deeplx.exe")
else:
    deeplx_path = os.path.join(os.path.dirname(__file__), "deeplx.exe")
deeplx_process = subprocess.Popen([deeplx_path], creationflags=subprocess.CREATE_NO_WINDOW)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

current_ascii_text = ""

def process_image(source="clipboard"):
    global current_ascii_text
    current_ascii_text = ""

    if source == "clipboard":
        image = get_image_from_clipboard()
    else:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        image = get_image_from_file(file_path)

    if not image:
        return

    hex_values = extract_hex_from_image(image)
    if not hex_values:
        messagebox.showerror("Ошибка", "Не найден шестнадцатеричный текст.")
        return

    ascii_text = hex_to_ascii(hex_values)
    if not ascii_text:
        messagebox.showerror("Ошибка", "Не удалось конвертировать в ASCII.")
        return

    current_ascii_text = ascii_text
    original_text.delete("1.0", "end")
    original_text.insert("end", ascii_text)
    translate_button.configure(state="normal")

def translate_text():
    global current_ascii_text
    if not current_ascii_text:
        messagebox.showwarning("Предупреждение", "Нет текста для перевода.")
        return

    translated_text = translate_text_deeplx(current_ascii_text, source_lang='en', target_lang='ru')
    if not translated_text:
        messagebox.showerror("Ошибка", "Не удалось перевести текст.")
        return

    translation_text.delete("1.0", "end")
    translation_text.insert("end", translated_text)

def copy_result():
    text = original_text.get("1.0", "end").strip()
    if text:
        copy_to_clipboard(text)

root = ctk.CTk()
root.title("Hex2ASCII с DeepLX")
root.geometry("600x600")

def on_closing():
    if 'deeplx_process' in globals():
        deeplx_process.terminate()
    root.destroy()
    sys.exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)

process_clipboard_button = ctk.CTkButton(master=root, text="Обработать скриншот", 
                                         command=lambda: process_image("clipboard"), 
                                         corner_radius=10)
process_clipboard_button.pack(pady=10)

process_file_button = ctk.CTkButton(master=root, text="Обработать файл", 
                                    command=lambda: process_image("file"), 
                                    corner_radius=10)
process_file_button.pack(pady=10)

original_label = ctk.CTkLabel(master=root, text="Оригинал (EN)", font=("Arial", 14))
original_label.pack(pady=5)
original_text = ctk.CTkTextbox(master=root, height=150, width=500)
original_text.pack(pady=5)

translation_label = ctk.CTkLabel(master=root, text="Перевод (RU)", font=("Arial", 14))
translation_label.pack(pady=5)
translation_text = ctk.CTkTextbox(master=root, height=150, width=500)
translation_text.pack(pady=5)

translate_button = ctk.CTkButton(master=root, text="Перевести текст", 
                                 state="disabled", 
                                 command=translate_text, 
                                 corner_radius=10)
translate_button.pack(pady=10)

copy_button = ctk.CTkButton(master=root, text="Скопировать в буфер обмена", 
                            command=copy_result, 
                            corner_radius=10)
copy_button.pack(pady=10)

root.mainloop()
