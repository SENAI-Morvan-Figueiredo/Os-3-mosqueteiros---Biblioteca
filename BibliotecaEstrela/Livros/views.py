from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Generos, Livros

def AdicionarLivro(request):
    generos = Generos.objects.all()

    if request.method == "POST":
        nome = request.POST.get("nome")
        autor = request.POST.get("autor")
        editora = request.POST.get("editora")
        descricao = request.POST.get("descricao")
        data_publicacao = request.POST.get("data_publicacao")
        genero_id = request.POST.get("genero")
        status = request.POST.get("status")
        imagem = request.FILES.get("imagem")  # 👈 para upload de imagens

        # Cria o livro no banco
        Livros.objects.create(
            nome=nome,
            autor=autor,
            editora=editora,
            descricao=descricao,
            data_publicacao=data_publicacao,
            imagem=imagem,
            status=status
        )

        return redirect("Livros:AdicionarLivro")  # 👈 volta para a mesma tela

    return render(request, "AdicionarLivro.html", {"generos": generos})

def AdicionarCategoria(request):
    generos = Generos.objects.all()

    if request.method == "POST":
        nome_genero = request.POST.get("nome_genero")
        Generos.objects.create(
            nome_genero=nome_genero
        )
        
        return redirect("Livros:AdicionarCategoria")
    
    return render(request, "AdicionarCategoria.html", {
        "generos": generos
    })