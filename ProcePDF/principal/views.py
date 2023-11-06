from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from PIL import Image
import pytesseract

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import fitz  


def index(request):
    return render(request, 'principal/index.html')

def ventanaIdeas(request):
    return render(request, 'principal/ventanaIdeas.html')

def ventanaCollage(request):
    return render(request, 'principal/ventanaCollage.html')

def ventanaResumen(request):
    return render(request, 'principal/ventanaResumen.html')

def ventanaImagenes(request):
    return render(request, 'principal/ventanaImagenes.html')

def ventanaPpt(request):
    return render(request, 'principal/ventanaPpt.html')

def extract_text(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        # Guarda el archivo PDF en el servidor
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        # Ruta del archivo PDF en el servidor
        pdf_path = fs.url(filename)
        # Extraer texto del PDF
        text = extract_text_from_pdf(pdf_path)
        # Eliminar el archivo PDF después de obtener el texto
        full_path = os.path.join(settings.MEDIA_ROOT, pdf_path.strip('/'))
        if os.path.exists(full_path):
            os.remove(full_path)
        return JsonResponse({'text': text})
    return JsonResponse({'error': 'No se proporcionó un archivo PDF válido'})


def extract_text_from_pdf(pdf_path):
    # Directorio para almacenar las imágenes
    image_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_images')
    os.makedirs(image_dir, exist_ok=True)

    text = ''
    full_path = os.path.join(settings.MEDIA_ROOT, pdf_path.strip('/'))

    if os.path.exists(full_path):
        pdf = fitz.open(full_path)

        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            image_list = page.get_pixmap()

            # Guarda la imagen en el directorio de imágenes
            image_path = os.path.join(image_dir, f'page_{page_num + 1}.png')
            image_list.save(image_path)

            # Realiza la extracción de texto de la imagen con Pytesseract
            extracted_text = pytesseract.image_to_string(Image.open(image_path))

            # Agrega el texto extraído a la variable text
            text += extracted_text
        delete_images()
        return text
    else:
        return 'Archivo PDF no encontrado'
    
def delete_images():
    # Directorio donde se almacenan las imágenes
    image_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_images')

    # Verifica si el directorio existe
    if os.path.exists(image_dir):
        # Elimina todos los archivos en el directorio
        for file in os.listdir(image_dir):
            file_path = os.path.join(image_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")

        # Elimina el directorio vacío
        os.rmdir(image_dir)