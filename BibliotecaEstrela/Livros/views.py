from django.shortcuts import render, redirect
from .models import Livros
from .models import Generos
from .models import Livros_Generos
from .forms import GenerosForm, LivrosForm, LivrosGenerosForm
from django.views.generic import DetailView

from django.views.generic.edit import ModelFormMixin
from Biblioteca.forms import FormAval
from Biblioteca.models import Avaliacoes

def calc_nota(id):
    try:
        avals = [i.nota for i in Avaliacoes.objects.filter(id_livro_id=id)]
        nota = sum(avals)/len(avals)
        return {'nota': f'{nota:.2f}', 'num_avals': len(avals)}
    
    except:
        return 0

class LivroDetalhes(ModelFormMixin, DetailView):
    model = Livros
    template_name = 'Detalhes_Livro.html'

    form_class = FormAval
    
    def get_context_data(self, **kwargs):
        livro = super().get_context_data(**kwargs)
        avaliacoes = Avaliacoes.objects.filter(id_livro_id=livro['livros'].pk)
        form = self.get_form()

        return {"livro": livro['livros'], "form": form, 'avaliacoes': avaliacoes, 'nota': calc_nota(livro['livros'].pk)}
    
    def form_valid(self, form):
        form.instance.id_user_id = self.request.user.id
        form.instance.id_livro_id = self.object.id
        return super(LivroDetalhes, self).form_valid(form)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()

        if form.is_valid() and int(form.data['nota'])<=5 and int(form.data['nota'])>=0:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    success_url = '#'

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
