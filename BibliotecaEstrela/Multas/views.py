from django.shortcuts import render, get_object_or_404
from .models import Emprestimos
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse

import mercadopago
from django.conf import settings

# @login_required
# def minhas_multas(request):
#     # 1️⃣ Buscar empréstimos do usuário que ainda não foram devolvidos
#     emprestimos = Emprestimos.objects.filter(id_user=request.user, status="emprestado")

#     # 2️⃣ Criar lista de pagamentos para empréstimos atrasados
#     pagamentos = []
#     for emprestimo in emprestimos:
#         valor_multa = emprestimo.calcular_multa()
#         if valor_multa > 0:
#             payment, created = Payment.objects.get_or_create(
#                 emprestimo=emprestimo,
#                 defaults={"amount": valor_multa}
#             )
#             pagamentos.append(payment)

#     return render(request, "user/multas.html", {"pagamentos": pagamentos})


@login_required
def criar_pagamento(request):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    pagamento_data = {
        'items': [
            {
                'id': '1',
                'title': 'Livro 1',
                'quantity': 1,
                'unit_price': 100
            }
        ],
        'back_urls': {
            'success': 'http://127.0.0.1:8000/user/multas/',
            'failure': 'http://127.0.0.1:8000/user/multas/',
            'pending': 'http://127.0.0.1:8000/user/multas/',
        },
        
    }

    preference = sdk.preference().create(pagamento_data)
    response_data = preference.get('response', {})
    print("Resposta do Mercado Pago:", response_data)

    link_pagamento = response_data.get('sandbox_init_point')
    print(link_pagamento)

    # ✅ Se o Mercado Pago retornou erro, não tente redirecionar
    if not link_pagamento or not isinstance(link_pagamento, str):
        return HttpResponse(f"Erro ao criar pagamento:<br><pre>{response_data}</pre>", status=400)

    return render(request, 'user/multas.html', {'link_pagamento': link_pagamento})