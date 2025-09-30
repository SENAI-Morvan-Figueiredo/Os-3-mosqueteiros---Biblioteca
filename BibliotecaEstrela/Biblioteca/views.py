from django.shortcuts import render
from Livros.models import Livros

# Create your views here.

def index(request):
    livros = Livros.objects.all()
    return render(request, 'Biblioteca/index.html', {"livros": livros})