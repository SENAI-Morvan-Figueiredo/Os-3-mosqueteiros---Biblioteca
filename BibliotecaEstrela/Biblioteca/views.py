from django.shortcuts import render
from Livros.models import Livros
# Create your views here.

def index(request):
    livros = Livros.objects.all()
    return render(request, 'Biblioteca/index.html', {"livros": livros})

def catalogo(request):
    livros = Livros.objects.all()
    livros_alfabetico = Livros.objects.order_by("nome")
    livros_disponiveis = Livros.objects.filter(status="Disponível")

    return render(request, "Biblioteca/catalogo.html", {
        "livros": livros,
        "livros_alfabetico": livros_alfabetico,
        "livros_disponiveis": livros_disponiveis,
    })