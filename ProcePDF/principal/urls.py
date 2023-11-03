from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ventanaIdeas/', views.ventanaIdeas, name='ventanaIdeas'),
    path('ventanaCollage/', views.ventanaCollage, name='ventanaCollage'),

]
