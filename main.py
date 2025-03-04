import tkinter as tk
from tkinter import messagebox
from image_processor import get_image_from_clipboard, extract_hex_from_image, hex_to_ascii, copy_to_clipboard

# Основная функция обработки
def process_image():
    image = get_image_from_clipboard()
    if image:
        hex_values = extract_hex_from_image(image)
        if hex_values:
            ascii_text = hex_to_ascii(hex_values)
            if ascii_text:
                result_text.delete(1.0, tk.END)  # Очищаем текстовое поле
                result_text.insert(tk.END, ascii_text)  # Вставляем результат
                copy_button.config(state=tk.NORMAL)  # Активируем кнопку копирования
            else:
                messagebox.showerror("Ошибка", "Не удалось найти валидные шестнадцатеричные значения.")
        else:
            messagebox.showerror("Ошибка", "Не удалось найти шестнадцатеричные значения на изображении.")

# Создание графического интерфейса
root = tk.Tk()
root.title("Конвертер шестнадцатеричного текста в ASCII")

# Создание кнопки для обработки изображения
process_button = tk.Button(root, text="Обработать скриншот", command=process_image)
process_button.pack(pady=10)

# Текстовое поле для отображения результата
result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=10)

# Кнопка для копирования результата в буфер обмена
copy_button = tk.Button(root, text="Скопировать в буфер обмена", state=tk.DISABLED, command=lambda: copy_to_clipboard(result_text.get(1.0, tk.END)))
copy_button.pack(pady=10)

# Запуск графического интерфейса
root.mainloop()