from django.shortcuts import render, redirect
from .models import Livros
from .models import Generos
from .models import Livros_Generos
from .forms import GenerosForm, LivrosForm, LivrosGenerosForm

def AdicionarCategoria(request):
    if request.method == "POST":
        form = GenerosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Livros:AdicionarCategoria")
    else:
        form = GenerosForm()

    generos = Generos.objects.all()
    return render(request, "AdicionarCategoria.html", {"form": form, "generos": generos})

def AdicionarLivro(request):
    if request.method == "POST":
        livro_form = LivrosForm(request.POST, request.FILES)

        if livro_form.is_valid():
            livro = livro_form.save()  # salva o livro primeiro

            # pega os gêneros enviados
            generos_ids = request.POST.getlist("id_genero")
            for genero_id in generos_ids:
                Livros_Generos.objects.create(id_livros=livro, id_genero_id=genero_id)

            return redirect("Livros:AdicionarLivro")
    else:
        livro_form = LivrosForm()
        genero_form = LivrosGenerosForm()

    return render(request, "AdicionarLivro.html", {
        "livro_form": livro_form,
        "genero_form": genero_form
    })



def Livros_view(request):
    # Para criar novo livro via form
    if request.method == "POST":
        form = LivrosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("Livros:Livros")  # redireciona para a mesma página
    else:
        form = LivrosForm()

    livros = Livros.objects.all()
    return render(request, "Livros.html", {"livros": livros, "form": form})