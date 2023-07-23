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