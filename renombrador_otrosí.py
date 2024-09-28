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
    # Amplía la expresión regular para capturar más variaciones
    match = re.search(r'(C[.]?C|PPT|NIT|CE)[.:\s]*([\d.-]+)', text, re.IGNORECASE)
    if match:
        tipo_documento = match.group(1).replace('.', '').upper()
        numero_documento = re.sub(r'[^\d]', '', match.group(2))  # Elimina todos los no dígitos
        return tipo_documento, numero_documento
    return None, None

def find_fecha(text):
    # Busca patrones de fecha más flexibles
    date_patterns = [
        r'en la fecha\s+(\d{1,2}\s+de\s+[a-zA-Z]+\s+de\s+\d{4})',
        r'(\d{1,2}\s+de\s+[a-zA-Z]+\s+de\s+\d{4})',
        r'(\d{2}/\d{2}/\d{4})'
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def find_numero_otrosi(text):
    # Busca variaciones del patrón "OTROSI N°" o "N°"
    patterns = [
        r'OTROS[IÍ]\s*N[°º]\s*[:.]?\s*(\d+)',
        r'N[°º]\s*[:.]?\s*(\d+)\s*[:.]?\s*OTROS[IÍ]',
        r'N[°º]\s*[:.]?\s*(\d+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def rename_pdf(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(pdf_path)
            
            tipo_documento, numero_documento = find_cedula(text)
            fecha = find_fecha(text)
            numero_otrosi = find_numero_otrosi(text)
            
            if numero_documento:
                new_filename_parts = [numero_documento, "OTROSI"]
                
                if numero_otrosi:
                    new_filename_parts.append(f"N{numero_otrosi}")
                
                if fecha:
                    new_filename_parts.append(fecha.replace('/', '-'))
                
                new_filename = "_".join(new_filename_parts) + ".pdf"
                new_path = os.path.join(folder_path, new_filename)
                
                counter = 1
                while os.path.exists(new_path):
                    new_filename = "_".join(new_filename_parts + [f"({counter})"]) + ".pdf"
                    new_path = os.path.join(folder_path, new_filename)
                    counter += 1
                
                os.rename(pdf_path, new_path)
                print(f"Renombrado: {filename} -> {new_filename}")
            else:
                print(f"No se encontró número de documento en: {filename}")

# Usa la función
folder_path = 'pdfsotrosí'  # Reemplaza esto con la ruta de tu carpeta
rename_pdf(folder_path)