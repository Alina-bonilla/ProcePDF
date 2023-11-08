from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ventanaIdeas/', views.ventanaIdeas, name='ventanaIdeas'),
    path('ventanaCollage/', views.ventanaCollage, name='ventanaCollage'),
    path('ventanaResumen/', views.ventanaResumen, name='ventanaResumen'),
    path('ventanaImagenes/', views.ventanaImagenes, name='ventanaImagenes'),
    path('ventanaPpt/', views.ventanaPpt, name='ventanaPpt'),

    path('extraerTexto/', views.extraerTexto, name='extraerTexto'),
    path('generarResumen/', views.generarResumen, name='generarResumen'),  
    path('generarIdeasPrincipales/', views.generarIdeasPrincipales, name='generarIdeasPrincipales'),  
    path('generarCollage/', views.generarCollage, name='generarCollage'),
    path('buscarImagenes/', views.buscarImagenes, name='buscarImagenes'),
    path('generar_presentacion/', views.generar_presentacion, name='generar_presentacion'),


    path('descargar_ideas/', views.descargarIdeas, name='descargar_ideas'),
    path('descargar_imagenes/', views.descargar_imagenes, name='descargar_imagenes'),
    path('descargar_resumen/', views.descargarResumen, name='descargar_resumen'),
    path('download_collage/', views.download_collage, name='download_collage'),


]
