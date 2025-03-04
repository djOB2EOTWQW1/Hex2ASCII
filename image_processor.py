import pytesseract
from PIL import ImageGrab
import re
import pyperclip
import tkinter.messagebox as messagebox
import logging

# Настройка логирования (логирование всех уровней)
logging.basicConfig(filename='log.txt', level=logging.NOTSET, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для получения изображения из буфера обмена
def get_image_from_clipboard():
    image = ImageGrab.grabclipboard()  # Получаем изображение из буфера обмена
    if image is None:
        messagebox.showerror("Ошибка", "Нет изображения в буфере обмена.")
        logging.error("Нет изображения в буфере обмена.")  # Логируем ошибку
        return None
    logging.info("Изображение получено из буфера обмена.")  # Логируем успешное получение изображения
    return image

# Функция для извлечения шестнадцатеричного текста из изображения
def extract_hex_from_image(image):
    text = pytesseract.image_to_string(image)  # Извлекаем текст с изображения
    logging.info(f"Извлеченный текст: {text}")  # Логирование извлеченного текста
    hex_values = re.findall(r'[0-9A-Fa-f]+', text)  # Ищем все шестнадцатеричные числа
    logging.info(f"Шестнадцатеричные значения: {hex_values}")  # Логирование найденных шестнадцатеричных значений
    return hex_values

# Функция для конвертации шестнадцатеричных значений в ASCII
def hex_to_ascii(hex_values):
    ascii_text = ""
    for hex_value in hex_values:
        # Дополняем одиночные значения шестёркой только если длина 1
        if len(hex_value) == 1:
            hex_value = '6' + hex_value.upper()  # Дополняем '6' вместо '0' и приводим к верхнему регистру
        
        try:
            logging.debug(f"Пытаемся конвертировать: {hex_value}")  # Логирование каждого шестнадцатеричного значения
            ascii_char = bytes.fromhex(hex_value).decode('ascii')
            
            # Специальное логирование для пробела
            if ascii_char == ' ':
                logging.info(f"Конвертировано: {hex_value} -> ")
                ascii_text += ' '
            else:
                logging.info(f"Конвертировано: {hex_value} -> {ascii_char}")  # Логирование успешной конверсии
                ascii_text += ascii_char
        except ValueError:
            logging.warning(f"Ошибка при конвертации: {hex_value}")  # Логирование ошибок при конвертации
            continue  # Игнорируем некорректные значения
    return ascii_text

# Функция для копирования текста в буфер обмена
def copy_to_clipboard(text):
    pyperclip.copy(text)
    messagebox.showinfo("Информация", "Текст скопирован в буфер обмена.")
    logging.info("Текст скопирован в буфер обмена.")  # Логируем информацию о копировании