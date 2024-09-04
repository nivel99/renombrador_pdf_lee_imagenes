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
    # Modifica la expresión regular para capturar "CC", "C.C", "PPT", etc.
    match = re.search(r'(C[.]?C|PPT)[.:\s]*([\d.]+)', text, re.IGNORECASE)
    if match:
        tipo_documento = match.group(1).replace('.', '')  # Remueve los puntos de "C.C"
        numero_documento = match.group(2).replace('.', '')  # Remueve los puntos del número de documento
        return tipo_documento, numero_documento
    return None, None

def rename_pdf(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            tipo_documento, numero_documento = find_cedula(text)
            if numero_documento:
                new_filename = f"{numero_documento}_Terminación.pdf"
                new_path = os.path.join(folder_path, new_filename)
                
                # Verificar si el archivo ya existe y añadir un sufijo en caso necesario
                counter = 1
                while os.path.exists(new_path):
                    new_filename = f"{numero_documento}_Terminación({counter}).pdf"
                    new_path = os.path.join(folder_path, new_filename)
                    counter += 1
                
                os.rename(pdf_path, new_path)
                print(f"Renombrado: {filename} -> {new_filename}")
            else:
                print(f"No se encontró No en: {filename}")

# Usa la función
folder_path = 'pdfsTerminacion'
rename_pdf(folder_path)
