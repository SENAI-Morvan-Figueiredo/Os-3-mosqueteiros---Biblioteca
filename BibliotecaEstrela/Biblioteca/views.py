from django.shortcuts import render, redirect
from .models import Emprestimos, Reserva, Avaliacoes, Pedidos_extensao

from User.models import Usuario
from Livros.models import Livros

# Create your views here.

def checar_livros_em_posse(id_user):
    #Busca de empréstimos feitos pelo user
    emprestimos_feitos = Emprestimos.objects.filter(id_user=id_user).all()

    em_posse = []

    #Checagem e armazenamento de quais não foram devolvidos
    for i in emprestimos_feitos:
        if i.status != 'Devolvido':
            em_posse.append(i)

    return em_posse

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
    return render(request, 'Biblioteca/index.html')


def criar_emprestimo(request, id_livro, id_user):
    
    #Checagem removida por enquanto para maior facilidade de testes

    #em_posse = checar_livros_em_posse(id_user)
    #if len(em_posse) <= 5 :

    novo = Emprestimos(id_user=Usuario.objects.get(id=id_user), id_livro=Livros.objects.get(id=id_livro), status="Disponível para retirar")
    novo.save()
    
    livro = Livros.objects.get(id=id_livro)
    livro.status="indisponivel"
    livro.save()

    return redirect("livros")


def criar_reserva(request, id_livro, id_user):

    #em_posse = checar_livros_em_posse(id_user)
    #if len(em_posse) <= 5 :
    
    novo = Reserva(id_user=Usuario.objects.get(id=id_user), id_livro=Livros.objects.get(id=id_livro), status="Em espera")
    novo.save()

    return redirect("livros")