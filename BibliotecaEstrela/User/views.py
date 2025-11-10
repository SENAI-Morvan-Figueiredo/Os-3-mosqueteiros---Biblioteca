from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, CompleteSignupForm, UserUpdateImageForm
from .models import Usuario
from Biblioteca.models import Reserva, Emprestimos, Pedidos_extensao, Avaliacoes
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from Biblioteca.models import Notificacoes

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            return redirect('login')
            
    else:
        form = UserRegisterForm()
        
    return render(request, 'user/register.html', {'form': form})

@login_required
def tela_perfil(request):
    user = request.user
    reservas = Reserva.objects.filter(id_user=request.user)

    if user.is_superuser:
        print("ok - adm")
        return redirect('Bibliotecario:teste')

    if request.method == 'POST':

        if 'salvar_dados' in request.POST:
            form = UserUpdateForm(request.POST, instance=user)
            imagem_form = UserUpdateImageForm(instance=user)

            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('tela_perfil')
            
            else:
                print("Form inválido:", form.errors)

        elif 'salvar_imagem' in request.POST:
            form = UserUpdateForm(instance=user)
            imagem_form = UserUpdateImageForm(request.POST, request.FILES, instance=user)

            if imagem_form.is_valid():
                print('a')
                imagem_form.save()
                return redirect('tela_perfil')
            
            else:
                print("Imagem inválida:", imagem_form.errors)

        elif 'deletar' in request.POST:
            print("a")
            user.delete()
            return redirect('login')
        

        # form = UserUpdateForm(request.POST, instance=user)
        # if form.is_valid():
        #     form.save()
        #     user = form.save()
        #     update_session_auth_hash(request, user)
        #     print("a")
        #     return redirect('tela_perfil')
        # else:
        #     print("Form inválido:", form.errors)


    else:
        form = UserUpdateForm(instance=user)
        imagem_form = UserUpdateImageForm(instance=user)


    if request.method == 'GET':
        reservas = Reserva.objects.filter(id_user=request.user, status="Em espera")
        devolvidos = Emprestimos.objects.filter(id_user=request.user, status="Devolvido")
        em_posse = Emprestimos.objects.filter(id_user=request.user, status="Disponível para retirar")
        avaliacoes = Avaliacoes.objects.filter(id_user=request.user)

    context = {
        'form': form,
        'imagem_form': imagem_form,
        'reservas': reservas,
        'devolvidos': devolvidos,
        'em_posse': em_posse,
        'avaliacoes': avaliacoes,
        
    }
    return render(request, 'user/tela_perfil.html', context)

@login_required
def historico_perfil(request):
    reservas = Reserva.objects.filter(id_user=request.user)
    emprestimos = Emprestimos.objects.filter(id_user=request.user, status="Disponível para retirar")
    
    # Aqui vamos usar os empréstimos como base para o select
    extensoes = emprestimos

    if request.method == 'POST':
        id_emprestimo = request.POST.get('livro')

        # Evita duplicar pedidos de extensão para o mesmo empréstimo
        ja_existe = Pedidos_extensao.objects.filter(id_emprestimo=id_emprestimo).exists()

        if not ja_existe:
            emprestimo = Emprestimos.objects.get(id=id_emprestimo)
            Pedidos_extensao.objects.create(
                id_emprestimo=emprestimo,
                status="Pendente"
            )

    context = {
        'reservas': reservas,
        'emprestimos': emprestimos,
        'extensoes': extensoes,
    }

    return render(request, 'user/historico_perfil.html', context)



@login_required
def notificacoes_perfil(request):
    user = request.user.id
    notificacoes = Notificacoes.objects.filter(id_user=user).all()

    return render(request, 'user/notificacoes.html', {'notificacoes': notificacoes})

def atualizar_notif(request, notif, tipo):
    notificacao = Notificacoes.objects.get(id=notif)
    if tipo == 'deletar':
        notificacao.delete()
    elif tipo == 'lido':
        notificacao.lido = True
        notificacao.save()

    return redirect('notificacoes_perfil')

# Completa as informações que estão faltando ao fazer login utilizando a conta do google.
@login_required
def complete_signup(request):
    user = request.user

    if user.telefone and user.cpf:
        return redirect('tela_perfil')
    
    if request.method == 'POST':
        form = CompleteSignupForm(request.POST, instance=user)

        if form.is_valid:
            form.save()
            return redirect('tela_perfil')
    else:
        form = CompleteSignupForm(instance=user)

    return render(request, 'user/complete_signup.html', {'form': form})