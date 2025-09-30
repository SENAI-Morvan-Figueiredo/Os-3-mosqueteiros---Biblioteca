from django.shortcuts import render, redirect
from .models import Livros
from .models import Generos
from .forms import GenerosForm, LivrosForm
from django.views.generic import DetailView

class LivroDetalhes(DetailView):
    model = Livros
    template_name = 'Detalhes_Livro.html'
    context_object_name = 'livro'

def AdicionarCategoria(request):
    if request.method == "POST":
        form = GenerosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("livros:AdicionarCategoria")
    else:
        form = GenerosForm()

    generos = Generos.objects.all()
    return render(request, "AdicionarCategoria.html", {"form": form, "generos": generos})

def AdicionarLivro(request):
    if request.method == "POST":
        form = LivrosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("livros:AdicionarLivro")
    else:
        form = LivrosForm()

    return render(request, "AdicionarLivro.html", {"form": form})


def Livros_view(request):
    # Para criar novo livro via form
    if request.method == "POST":
        form = LivrosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("livros:Livros")  # redireciona para a mesma página
    else:
        form = LivrosForm()

    livros = Livros.objects.all()
    return render(request, "Livros.html", {"livros": livros, "form": form})
