import pytesseract
import sys
import os
import logging
from pathlib import Path
from PIL import ImageGrab
import pyperclip
import tkinter.messagebox as messagebox
import re

logging.basicConfig(filename='log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_tesseract_path():
    # Проверяем, если программа запущена как скомпилированный .exe
    if getattr(sys, 'frozen', False):
        # Получаем путь, где PyInstaller распакует все файлы
        base_path = sys._MEIPASS
        # Строим путь к tesseract.exe, который будет встроен в .exe
        tesseract_path = os.path.join(base_path, "Tesseract-OCR", "tesseract.exe")
    else:
        # Если программа не скомпилирована, используем путь из текущей папки
        base_path = Path(__file__).resolve().parent
        tesseract_path = os.path.join(base_path, "Tesseract-OCR", "tesseract.exe")

    # Проверяем, существует ли файл tesseract.exe
    if os.path.exists(tesseract_path):
        logging.info(f"Используется встроенный Tesseract: {tesseract_path}")
        return tesseract_path
    else:
        logging.warning("Tesseract не найден, используется системный путь.")
        return "tesseract"  # Если tesseract не найден, будет использоваться глобальная установка.

# Устанавливаем путь к tesseract в pytesseract
pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def get_image_from_clipboard():
    image = ImageGrab.grabclipboard()
    if image is None:
        messagebox.showerror("Ошибка", "Нет изображения в буфере обмена.")
        logging.error("Нет изображения в буфере обмена.")
        return None
    logging.info("Изображение получено из буфера обмена.")
    return image

def extract_hex_from_image(image):
    text = pytesseract.image_to_string(image)
    logging.info(f"Извлеченный текст: {text}")
    
    hex_values = re.findall(r'[0-9A-Fa-f]+', text)
    logging.info(f"Шестнадцатеричные значения: {hex_values}")
    
    return hex_values

def hex_to_ascii(hex_values):
    ascii_text = ""
    for hex_value in hex_values:
        if len(hex_value) == 1:
            hex_value = '6' + hex_value.upper()
        
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
