# import os
# import sys
# import pytesseract
# from PIL import Image
# from gtts import gTTS

# def parse_scanned_document(image_path):
#     image = Image.open(image_path)
#     text = pytesseract.image_to_string(image, lang='rus')
#     return text

# def save_text_to_file(text, output_file):
#     with open(output_file, 'w', encoding='utf-8') as file:
#         file.write(text)
        

# def convert_text_to_audio(text, output_file):
#     tts = gTTS(text=text, lang='ru')
#     tts.save(output_file)


# if __name__ == "__main__":
#     input_folder_path = os.path.join(os.getcwd(), "input_scan_image")
#     output_folder_path = os.path.join(os.getcwd(), "output_parsed_text")
#     audio_folder_path = os.path.join(os.getcwd(), "output_audio")
#     os.makedirs(output_folder_path, exist_ok=True)
#     os.makedirs(audio_folder_path, exist_ok=True)
    

#     for filename in os.listdir(input_folder_path):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             input_image_path = os.path.join(input_folder_path, filename)
#             output_file_path = os.path.join(output_folder_path, os.path.splitext(filename)[0] + ".txt")
#             output_audio_path = os.path.join(audio_folder_path, os.path.splitext(filename)[0] + ".mp3")

#             parsed_text = parse_scanned_document(input_image_path)
#             save_text_to_file(parsed_text, output_file_path)
#             convert_text_to_audio(parsed_text, output_audio_path)
import os
import pytesseract
from PIL import Image
from gtts import gTTS
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
if token is None:
    print("Please set your TOKEN value in the .env file")
    exit()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Пришли мне изображение для обработки.")

@bot.message_handler(content_types=['photo'])
def process_image(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = bot.download_file(file_info.file_path)

    with open('input_image.jpg', 'wb') as image_file:
        image_file.write(file_path)

    parsed_text = parse_scanned_document('input_image.jpg')
    audio_file_path = os.path.join(os.getcwd(), 'output_audio.mp3')
    convert_text_to_audio(parsed_text, audio_file_path)

    text_file_path = os.path.join(os.getcwd(), 'output_text.txt')
    with open(text_file_path, 'w') as text_file:
        text_file.write(parsed_text)

    bot.send_message(message.chat.id, "Текст успешно извлечен и преобразован в аудиофайл и текстовый файл.")

    with open(audio_file_path, 'rb') as audio_file:
        bot.send_audio(message.chat.id, audio_file)

    with open(text_file_path, 'rb') as text_file:
        bot.send_document(message.chat.id, text_file)

def parse_scanned_document(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='rus')
    return text

def convert_text_to_audio(text, output_file):
    tts = gTTS(text=text, lang='ru')
    tts.save(output_file)

bot.polling()