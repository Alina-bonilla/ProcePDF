from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os

def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']

        # Guardar el archivo PDF en un directorio temporal
        fs = FileSystemStorage()
        pdf_name = fs.save(pdf_file.name, pdf_file)
        pdf_url = fs.url(pdf_name)

        # Procesar el archivo PDF aquí (puedes agregar tu lógica de procesamiento)

        # Eliminar el archivo PDF después de procesarlo
        file_path = os.path.join(fs.location, pdf_name)
        if os.path.exists(file_path):
            os.remove(file_path)

    return render(request, 'myapp/upload_pdf.html', {'title': 'ProcePDF'})
