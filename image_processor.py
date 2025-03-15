import pytesseract
import sys
import os
from pathlib import Path
from PIL import Image, ImageGrab
import pyperclip
import tkinter.messagebox as messagebox
import re
import requests
import subprocess

def start_deeplx_server(deeplx_path):
    try:
        if sys.platform == "win32":
            subprocess.Popen([deeplx_path], creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            subprocess.Popen([deeplx_path])
        print("DeepLX сервер запущен.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить DeepLX сервер: {e}")

def get_tesseract_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        tesseract_path = os.path.join(base_path, "Tesseract-OCR", "tesseract.exe")
    else:
        base_path = Path(__file__).resolve().parent
        tesseract_path = os.path.join(base_path, "Tesseract-OCR", "tesseract.exe")

    if os.path.exists(tesseract_path):
        return tesseract_path
    else:
        return "tesseract"

pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def get_image_from_clipboard():
    image = ImageGrab.grabclipboard()
    if image is None:
        messagebox.showerror("Ошибка", "Нет изображения в буфере обмена.")
        return None
    return image

def get_image_from_file(file_path):
    if file_path:
        try:
            image = Image.open(file_path)
            return image
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
            return None
    return None

def extract_hex_from_image(image):
    text = pytesseract.image_to_string(image)
    processed_text = text.upper()
    OCR_REPLACEMENTS = {"O": "6", "G": "6"}
    for wrong_char, correct_char in OCR_REPLACEMENTS.items():
        processed_text = processed_text.replace(wrong_char, correct_char)

    hex_groups = re.findall(r"[0-9A-F]+", processed_text)
    valid_pairs = [
        pair
        for group in hex_groups
        for pair in (
            [f"0{group}"[:2]] if len(group) % 2 != 0 
            else [group[i:i+2] for i in range(0, len(group), 2)]
        )
        if group
    ]
    return valid_pairs

def hex_to_ascii(hex_values):
    ascii_text = ""
    for hex_value in hex_values:
        try:
            ascii_char = bytes.fromhex(hex_value).decode('ascii')
            ascii_text += ascii_char
        except ValueError:
            continue
    return ascii_text

def translate_text_deeplx(text, source_lang='en', target_lang='ru'):
    url = "http://localhost:1188/translate"
    payload = {
        "text": text,
        "source_lang": source_lang.upper(),
        "target_lang": target_lang.upper()
    }
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        response.raise_for_status()
        result = response.json()
        translated_text = result.get("data", None)
        if translated_text:
            return translated_text
        return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Ошибка", f"Ошибка при запросе к DeepLX: {e}")
        return None

def copy_to_clipboard(text):
    pyperclip.copy(text)
    messagebox.showinfo("Информация", "Текст скопирован в буфер обмена.")
