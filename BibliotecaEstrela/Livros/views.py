from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Generos, Livros

def AdicionarLivro(request):
    pass

def AdicionarCategoria(request):
    generos = Generos.objects.all()

    if request.method == "POST":
        nome_genero = request.POST.get("nome_genero")
        Generos.objects.create(
            nome_genero=nome_genero
        )
        return render()
    
    return render(request, "AdicionarCategoria.html", {
        "generos": generos
    })