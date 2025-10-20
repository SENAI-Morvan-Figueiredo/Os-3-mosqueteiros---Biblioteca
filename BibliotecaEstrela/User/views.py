from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, CompleteSignupForm, UserUpdateImageForm
from .models import Usuario
from django.views.generic import DeleteView
from django.urls import reverse_lazy

from Biblioteca.models import Reserva, Emprestimos, Pedidos_extensao

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
                print(imagem_form.save())
                return redirect('tela_perfil')
            
            else:
                print("Imagem inválida:", imagem_form.errors)

        if 'deletar' in request.POST:
            print("a")
            user.delete()
            return redirect('login')
        

        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user = form.save()
            update_session_auth_hash(request, user)
            print("a")
            return redirect('tela_perfil')
        else:
            print("Form inválido:", form.errors)


    else:
        form = UserUpdateForm(instance=user)
        imagem_form = UserUpdateImageForm(instance=user)


    

    context = {
        'form': form,
        'imagem_form': imagem_form,
        'reservas': reservas,
    }
    return render(request, 'user/tela_perfil.html', context)

@login_required
def historico_perfil(request):
    extensao = Pedidos_extensao.objects.none()
    if request.method == 'GET':
        reservas = Reserva.objects.filter(id_user=request.user)

        emprestimo = Emprestimos.objects.filter(id_user=request.user)
    
    if request.method == 'POST':
        extensao = Pedidos_extensao.objects.filter(id_emprestimo__id_user=request.user)
    
    context = {
        'reservas': reservas,
        'emprestimos': emprestimo,
        'extensoes': extensao,
    }

    return render(request, 'user/historico_perfil.html', context)

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