from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'principal/index.html')

def ventanaIdeas(request):
    return render(request, 'principal/ventanaIdeas.html')

def ventanaCollage(request):
    return render(request, 'principal/ventanaCollage.html')