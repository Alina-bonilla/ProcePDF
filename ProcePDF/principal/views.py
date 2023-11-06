from django.shortcuts import render
from PIL import Image
import pytesseract
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import fitz  
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

nltk.download('stopwords')
nltk.download('punkt')

#------------------------------------------------------------- FUNCIONES PARA PASAR A OTRAS VENTANAS -----------------------------------------------------------
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


#----------------------------------------------------------------- FUNCIONES DE OPERACIONES -----------------------------------------------------------------
#Extrae el texto del archivo PDF
def extraerTexto(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        pdf_path = fs.url(filename)
        text = extraerTextoImagen(pdf_path)       
        request.session['extracted_text'] = text  # Guarda el texto en la sesión para que esté disponible en la vista de 'generarResumen'

        # Eliminar el archivo PDF después de obtener el texto
        full_path = os.path.join(settings.MEDIA_ROOT, pdf_path.strip('/'))
        if os.path.exists(full_path):
            os.remove(full_path)
        return JsonResponse({'text': text})
    return JsonResponse({'error': 'No se proporcionó un archivo PDF válido'})

#Extrae el texto de las imagenes del PDF
def extraerTextoImagen(pdf_path):
    image_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_images')
    os.makedirs(image_dir, exist_ok=True)
    text = ''
    full_path = os.path.join(settings.MEDIA_ROOT, pdf_path.strip('/'))

    if os.path.exists(full_path):
        pdf = fitz.open(full_path)
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            image_list = page.get_pixmap()
            image_path = os.path.join(image_dir, f'page_{page_num + 1}.png')
            image_list.save(image_path)

            # Realiza la extracción de texto de la imagen con Pytesseract
            extracted_text = pytesseract.image_to_string(Image.open(image_path))
            text += extracted_text
        eliminarImagen()
        return text
    else:
        return 'Archivo PDF no encontrado'

# Elimina todos los archivos en el directorio de imagenes
def eliminarImagen():
    image_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_images')
    if os.path.exists(image_dir):
        for file in os.listdir(image_dir):
            file_path = os.path.join(image_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")
        os.rmdir(image_dir)

#Genera un resumen del texto extraido
def generarResumen(request):
    idioma = set(stopwords.words("spanish")) #Idioma del texto
    text = request.session.get('extracted_text', '') #Texto de la ventana inicial
    palabras = word_tokenize(text)

    # Se crea un diccionario para crear una tabla de frecuencias de las palabras.
    frecuenciaTabla = dict()
    for palabra in palabras:
        palabra = palabra.lower() #formato de palabras
        if palabra in idioma: 
            continue 
        if palabra in frecuenciaTabla: # Si la palabra ya se encuentra en la tabla frecuencia se le Suma 1 a la posición donde se encuentra la palabra.
            frecuenciaTabla[palabra] += 1 
        else:
            frecuenciaTabla[palabra] = 1 # Sino, la palabra en la TF va a ser igual a 1.
    
    # Crea una variable y un diccionario.
    oraciones = sent_tokenize(text)
    oracionValor = dict()

    #Se resorren las oraciones que se encuentran en el texto.
    for oracion in oraciones:
        for palabra, freq in frecuenciaTabla.items():
            if palabra in oracion.lower(): 
                if oracion in oracionValor: 
                    oracionValor[oracion] += freq # Se le sume 1 al número de frecuencia en la posición de la oración del sV.
                else:
                    oracionValor[oracion] = freq # Sino, que el valor de la posición de la oración sea igual a la frecuencia.

    sumaValores = 0
    for oracion in oracionValor:
        sumaValores += oracionValor[oracion] # Se suma 1 al valor de la Oración en su respectiva posición       
    promedio = int(sumaValores/ len(oracionValor)) # Divide la suma de valores en la total de oraciones valorizadas. 

    #Si la oración está las oraciones Valorizadas y la posición de la oración es mayor que 1.2 veces el promedio
    resumen = ''
    for oracion in oraciones:
        if (oracion in oracionValor) and (oracionValor[oracion] > (1.2 * promedio)):    
            resumen += " " + oracion # El resumen va a agregar un espacio más la oración que aprobó la condición.
    print(resumen)
    return render(request, 'principal/ventanaResumen.html', {'text': text, 'resumen': resumen})

