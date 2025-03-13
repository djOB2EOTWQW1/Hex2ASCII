import customtkinter as ctk
from tkinter import messagebox, filedialog
from image_processor import get_image_from_clipboard, get_image_from_file, extract_hex_from_image, hex_to_ascii, copy_to_clipboard

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def process_image(source="clipboard"):
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

    result_text.delete("1.0", "end")
    result_text.insert("end", ascii_text)
    copy_button.configure(state="normal")

def copy_result():
    text = result_text.get("1.0", "end").strip()
    if text:
        copy_to_clipboard(text)

root = ctk.CTk()
root.title("Hex2ASCII")
root.geometry("600x400")

process_clipboard_button = ctk.CTkButton(master=root, text="Обработать скриншот", 
                                         command=lambda: process_image("clipboard"), 
                                         corner_radius=10)
process_clipboard_button.pack(pady=10)

process_file_button = ctk.CTkButton(master=root, text="Обработать файл", 
                                    command=lambda: process_image("file"), 
                                    corner_radius=10)
process_file_button.pack(pady=10)

result_text = ctk.CTkTextbox(master=root, height=150, width=400)
result_text.pack(pady=10)

copy_button = ctk.CTkButton(master=root, text="Скопировать в буфер обмена", 
                            state="disabled", 
                            command=copy_result, 
                            corner_radius=10)
copy_button.pack(pady=10)

root.mainloop()
