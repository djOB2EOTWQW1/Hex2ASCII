Сделан для LIL. Упрощает конвертацию Hex to ASCII.

Порядок действий:
1. Сделать скриншот непосредственно шестнадцатеричной строки. ![image](https://github.com/user-attachments/assets/b1abcc54-1c57-4478-83c2-3170085bbdff)
2. Нажать "обработать скриншот" (скриншот должен быть первым в буфере обмена)
3. Получить ASCII текст.

61 6d 20 69 20 6f 6b 61 79

:)

Важно!

До версии 1.2 требовалось установить 
[tesseract_OCR](https://github.com/tesseract-ocr/tesseract) для работы.

Известные проблемы

Программа использует стандартную кодировку ASCII, которая поддерживает только символы в пределах диапозона 0-127, что включает в себя только английский алфавит и некоторые другие символы.

Шестнадцатеричная строка, если фон неоднотонный, может не конвертироваться.

Могут быть квадратики вместо буквы / пропущенная буква / не та буква, которая должна быть.

В таком случае рекомендую забить / сделать скриншот еще раз.
