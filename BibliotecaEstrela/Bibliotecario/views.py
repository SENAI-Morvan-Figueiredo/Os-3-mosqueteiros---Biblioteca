from django.shortcuts import render, redirect, HttpResponse
from Livros.models import Livros, Generos, Livros_Generos
from User.models import Usuario
from Biblioteca.models import Emprestimos
from .forms import GenerosForm, LivrosForm, LivrosGenerosForm
from django.views.generic import DetailView

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
    if request.method == "POST":
        livro_form = LivrosForm(request.POST, request.FILES)
        categoria_form = GenerosForm(request.POST)

        if livro_form.is_valid():
            livro = livro_form.save()  # salva o livro primeiro

            # pega os gêneros enviados
            generos_ids = request.POST.getlist("id_genero")
            for genero_id in generos_ids:
                Livros_Generos.objects.create(id_livros=livro, id_genero_id=genero_id)

            return redirect("livros")
    
        if categoria_form.is_valid():
            categoria_form.save()
            return redirect("livros")
    else:
        livro_form = LivrosForm()
        genero_form = LivrosGenerosForm()
        form = GenerosForm()

    livros = Livros.objects.all()
    generos = Generos.objects.all()
    usuarios = Usuario.objects.all()
    emprestimos = Emprestimos.objects.all()
    context = {
        "livros": livros,
        "generos": generos,
        "usuarios": usuarios,
        "emprestimos": emprestimos,
        "livro_form": livro_form,
        "genero_form": genero_form,
        "form": form,
    }
    return render(request, 'adm_livros.html', context)
