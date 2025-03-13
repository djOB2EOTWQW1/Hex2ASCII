import pytesseract
import sys
import os
import logging
from pathlib import Path
from PIL import Image, ImageGrab
import pyperclip
import tkinter.messagebox as messagebox
import re

logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_tesseract_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        tesseract_path = os.path.join(base_path, "Tesseract-OCR", "tesseract.exe")
    else:
        base_path = Path(__file__).resolve().parent
        tesseract_path = os.path.join(base_path, "Tesseract-OCR", "tesseract.exe")

    if os.path.exists(tesseract_path):
        logging.info(f"Используется встроенный Tesseract: {tesseract_path}")
        return tesseract_path
    else:
        logging.warning("Tesseract не найден, используется системный путь.")
        return "tesseract"

pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def get_image_from_clipboard():
    image = ImageGrab.grabclipboard()
    if image is None:
        messagebox.showerror("Ошибка", "Нет изображения в буфере обмена.")
        logging.error("Нет изображения в буфере обмена.")
        return None
    logging.info("Изображение получено из буфера обмена.")
    return image

def get_image_from_file(file_path):
    if file_path:
        try:
            image = Image.open(file_path)
            logging.info(f"Изображение загружено из файла: {file_path}")
            return image
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")
            logging.error(f"Не удалось открыть файл: {e}")
            return None
    return None

def extract_hex_from_image(image):
    text = pytesseract.image_to_string(image)
    logging.info(f"Извлеченный текст: {text}")

    OCR_REPLACEMENTS = {"O": "6", "G": "6"}
    processed_text = text.upper()
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

    logging.info(f"Шестнадцатеричные пары: {valid_pairs}")
    return valid_pairs

def hex_to_ascii(hex_values):
    ascii_text = ""
    for hex_value in hex_values:
        try:
            ascii_char = bytes.fromhex(hex_value).decode('ascii')
            ascii_text += ascii_char
            logging.info(f"Конвертировано: {hex_value} -> {ascii_char}")
        except ValueError:
            logging.warning(f"Ошибка при конвертации: {hex_value}")
            continue

    return ascii_text

def copy_to_clipboard(text):
    pyperclip.copy(text)
    messagebox.showinfo("Информация", "Текст скопирован в буфер обмена.")
    logging.info("Текст скопирован в буфер обмена.")
