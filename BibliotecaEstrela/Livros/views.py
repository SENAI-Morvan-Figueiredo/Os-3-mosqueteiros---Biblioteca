from django.shortcuts import render, redirect
from .models import Livros
from .models import Generos
from .models import Livros_Generos
from .forms import GenerosForm, LivrosForm, LivrosGenerosForm
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
            return redirect("adicionar_categoria")
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

            return redirect("adicionar_livro")
    else:
        livro_form = LivrosForm()
        genero_form = LivrosGenerosForm()

    return render(request, "AdicionarLivro.html", {
        "livro_form": livro_form,
        "genero_form": genero_form
    })



def Livros_view(request):
    livros = Livros.objects.all()
    livros_alfabetico = Livros.objects.order_by("nome")
    livros_disponiveis = Livros.objects.filter(status="Disponível")

    return render(request, "Biblioteca/catalogo.html", {
        "livros": livros,
        "livros_alfabetico": livros_alfabetico,
        "livros_disponiveis": livros_disponiveis,
    })

def buscar_livro(request, busca):
    resultados = Livros.objects.filter(nome__contains=busca)

    return render(request, "Livros.html", {"livros": resultados})
