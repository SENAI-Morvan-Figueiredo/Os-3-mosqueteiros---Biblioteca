from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
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

    if request.method == 'GET':
        reservas = Reserva.objects.filter(id_user=request.user)

    context = {
        'form': form,
        'reservas': reservas,
    }
    return render(request, 'user/tela_perfil.html', context)

@login_required
def historico_perfil(request):
    reservas = Reserva.objects.filter(id_user=request.user)
    emprestimos = Emprestimos.objects.filter(id_user=request.user)
    
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
