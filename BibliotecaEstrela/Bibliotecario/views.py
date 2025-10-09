from django.shortcuts import render, redirect, HttpResponse
from Livros.models import Livros
from User.models import Usuario
from Biblioteca.models import Emprestimos

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