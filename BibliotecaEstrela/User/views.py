from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import Usuario

from django.contrib.auth.decorators import login_required

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
        form = UserRegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('tela_perfil')
    else:
        form = UserRegisterForm(instance=user)

    context = {
        'form': form,
    }
    return render(request, 'user/tela_perfil.html', context)