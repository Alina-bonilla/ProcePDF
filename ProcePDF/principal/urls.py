from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ventanaIdeas/', views.ventanaIdeas, name='ventanaIdeas'),
    path('ventanaCollage/', views.ventanaCollage, name='ventanaCollage'),
    path('ventanaResumen/', views.ventanaResumen, name='ventanaResumen'),
    path('ventanaImagenes/', views.ventanaImagenes, name='ventanaImagenes'),
    path('ventanaPpt/', views.ventanaPpt, name='ventanaPpt'),

    path('extract_text/', views.extract_text, name='extract_text'),

]
