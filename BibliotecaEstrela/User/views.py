from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, UserUpdateImageForm
from .models import Usuario
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
            
    else:
        form = UserRegisterForm()
        
    return render(request, 'user/register.html', {'form': form})

@login_required
def tela_perfil(request):
    user = request.user
    reservas = Reserva.objects.filter(id_user=request.user)

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
                imagem_form.save()
                return redirect('tela_perfil')
            
            else:
                print("Imagem inválida:", imagem_form.errors)

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