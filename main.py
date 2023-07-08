import os
import sys
import pytesseract
from PIL import Image

def parse_scanned_document(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='rus')
    return text

def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)

if __name__ == "__main__":
    input_folder_path = os.path.join(os.getcwd(), "input_scan_image")
    output_folder_path = os.path.join(os.getcwd(), "output_parsed_text")
    os.makedirs(output_folder_path, exist_ok=True)

    for filename in os.listdir(input_folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            input_image_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, os.path.splitext(filename)[0] + ".txt")

            parsed_text = parse_scanned_document(input_image_path)
            save_text_to_file(parsed_text, output_file_path)