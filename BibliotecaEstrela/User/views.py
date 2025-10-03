from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
from .models import Usuario

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
def complete_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'user/complete_profile.html', {'form': form})

@login_required
def tela_perfil(request):
    user = request.user

    if request.method == 'POST':
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