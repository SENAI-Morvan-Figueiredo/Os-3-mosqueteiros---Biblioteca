from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, CompleteSignupForm
from .models import Usuario
from django.views.generic import DeleteView
from django.urls import reverse_lazy

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

    if request.method == 'POST':
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

    

    context = {
        'form': form,
    }
    return render(request, 'user/tela_perfil.html', context)

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