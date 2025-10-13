from django.shortcuts import render, redirect, HttpResponse
from Livros.models import Livros, Generos
from User.models import Usuario
from Biblioteca.models import Emprestimos

# view para tela inicial (todo: trocar nomes)
def teste(request):
    livros = Livros.objects.all()
    usuarios = Usuario.objects.all()
    emprestimos = Emprestimos.objects.all()
    context = {
        "livros": livros,
        "usuarios": usuarios,
        "emprestimos": emprestimos,
    }
    return render(request, 'index.html', context)

# view para livro para adm:

def livros(request):

    livros = Livros.objects.all()
    generos = Generos.objects.all()
    usuarios = Usuario.objects.all()
    emprestimos = Emprestimos.objects.all()
    context = {
        "livros": livros,
        "generos": generos,
        "usuarios": usuarios,
        "emprestimos": emprestimos,
    }
    return render(request, 'adm_livros.html', context)
