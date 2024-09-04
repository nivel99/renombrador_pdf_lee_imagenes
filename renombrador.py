import os
import pytesseract
from pdf2image import convert_from_path
import re

# Asegúrate de tener instalado Tesseract-OCR y especifica la ruta si es necesario
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def find_cedula(text):
    match = re.search(r'No[.:\s]*(\d+)', text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def rename_pdf(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            cedula = find_cedula(text)
            if cedula:
                new_filename = f"{cedula}_Liquidacion.pdf"
                new_path = os.path.join(folder_path, new_filename)
                os.rename(pdf_path, new_path)
                print(f"Renombrado: {filename} -> {new_filename}")
            else:
                print(f"No se encontró No en: {filename}")

# Usa la función
folder_path = 'pdfs'
rename_pdf(folder_path)