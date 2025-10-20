from django.shortcuts import render, get_object_or_404
from .models import Emprestimos, Payment
from django.contrib.auth.decorators import login_required

@login_required
def minhas_multas(request):
    # 1️⃣ Buscar empréstimos do usuário que ainda não foram devolvidos
    emprestimos = Emprestimos.objects.filter(id_user=request.user, status='emprestado')

    # 2️⃣ Criar lista de pagamentos para empréstimos atrasados
    pagamentos = []
    for emprestimo in emprestimos:
        valor_multa = emprestimo.calcular_multa()
        if valor_multa > 0:
            payment, created = Payment.objects.get_or_create(
                emprestimo=emprestimo,
                defaults={'amount': valor_multa}
            )
            pagamentos.append(payment)

    return render(request, 'user/multas.html', {'pagamentos': pagamentos})