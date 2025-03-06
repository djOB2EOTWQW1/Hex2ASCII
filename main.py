import tkinter as tk
from tkinter import messagebox
from image_processor import get_image_from_clipboard, extract_hex_from_image, hex_to_ascii, copy_to_clipboard

def process_image():
    image = get_image_from_clipboard()
    if not image:
        return

    hex_values = extract_hex_from_image(image)
    if not hex_values:
        return messagebox.showerror("Ошибка", "Не найден шестнадцатеричный текст.")

    ascii_text = hex_to_ascii(hex_values)
    if not ascii_text:
        return messagebox.showerror("Ошибка", "Не удалось конвертировать в ASCII.")

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, ascii_text)
    copy_button.config(state=tk.NORMAL)

def copy_result():
    text = result_text.get(1.0, tk.END).strip()
    if text:
        copy_to_clipboard(text)

root = tk.Tk()
root.title("Hex to ASCII Converter")
root.geometry("600x400")

process_button = tk.Button(root, text="Обработать скриншот", command=process_image)
process_button.pack(pady=10)

result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=10)

copy_button = tk.Button(root, text="Скопировать в буфер обмена", state=tk.DISABLED, command=copy_result)
copy_button.pack(pady=10)

root.mainloop()
