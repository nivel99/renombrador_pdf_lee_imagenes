import os
import pytesseract
from pdf2image import convert_from_path
import re
from datetime import datetime

# Asegúrate de tener instalado Tesseract-OCR y especifica la ruta si es necesario
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def find_cedula(text):
    # Busca la cédula
    cedula_match = re.search(r'CC[.:\s]*(\d+)', text, re.IGNORECASE)
    cedula = cedula_match.group(1) if cedula_match else None

    # Busca el número (N°)
    numero_match = re.search(r'N[º°]\s*(\d+)', text, re.IGNORECASE)
    numero = numero_match.group(1) if numero_match else None

    # Busca la fecha en formato día/mes/año
    fecha_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', text)
    fecha = fecha_match.group(1) if fecha_match else None

    if fecha:
        # Convertir la fecha a un formato en letras
        try:
            fecha_dt = datetime.strptime(fecha, '%d/%m/%Y') if len(fecha) == 10 else datetime.strptime(fecha, '%d/%m/%y')
            meses = [
                "enero", "febrero", "marzo", "abril", "mayo", "junio",
                "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
            ]
            fecha_letras = f"{fecha_dt.day} de {meses[fecha_dt.month - 1]} de {fecha_dt.year}"
        except ValueError:
            fecha_letras = None
    else:
        fecha_letras = None

    return cedula, numero, fecha_letras

def rename_pdf(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            try:
                text = extract_text_from_pdf(pdf_path)
                cedula, numero, fecha = find_cedula(text)
                if cedula and numero and fecha:
                    new_filename = f"{cedula}-OTROSÍ-N{numero}-{fecha}.pdf"
                    new_path = os.path.join(folder_path, new_filename)
                    os.rename(pdf_path, new_path)
                    print(f"Renombrado: {filename} -> {new_filename}")
                else:
                    print(f"No se encontró toda la información en: {filename}")
            except Exception as e:
                print(f"Error al procesar {filename}: {e}")

# Usa la función
folder_path = 'pdfsotrosí'
rename_pdf(folder_path)
