import fitz  # PyMuPDF
import pytesseract
from PIL import Image

def extract_text_from_scanned_pdf(pdf_path):
    # Abre el archivo PDF usando PyMuPDF
    pdf_document = fitz.open(pdf_path)

    # Inicializa una cadena para almacenar el texto extraído
    extracted_text = ""

    # Recorre las páginas del PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Convierte la página en una imagen (puede haber múltiples imágenes por página)
        pix = page.get_pixmap()

        # Utiliza pytesseract para realizar OCR en cada imagen
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_text = pytesseract.image_to_string(img, lang='eng')  # Puedes especificar el idioma adecuado

        # Agrega el texto de la imagen al texto extraído de la página
        extracted_text += img_text

    # Cierra el archivo PDF
    pdf_document.close()

    return extracted_text


# Ejemplo de uso
pdf_path = "Lectura_Cap_24.pdf"
extracted_text = extract_text_from_scanned_pdf(pdf_path)
print(extracted_text)
