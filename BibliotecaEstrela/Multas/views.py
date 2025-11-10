from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import json

from User.models import Usuario
from Livros.models import Livros
from Biblioteca.models import Emprestimos
from .models import Multas, MultaLivro

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

@csrf_exempt
def mp_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        print("📦 Webhook recebido:", data)

        return JsonResponse({"status": "ok"})
    
    return JsonResponse({"error": "Método não suportado"}, status=400)

@transaction.atomic
def emitir_multa(emprestimo_objeto):
    usuario = emprestimo_objeto.id_user

    valor_atraso = emprestimo_objeto.calcular_multa()

    nova_multa = Multas.objects.create(
        id_emprestimo=emprestimo_objeto,
        id_usuario=usuario,
        nome_usuario_copia=usuario.username,
        cpf_usuario_copia=usuario.cpf,
        valor_multa=valor_atraso,
        status='PENDENTE'
    )

    dados_item_multa = emprestimo_objeto.get_dados_multa_livro()

    MultaLivro.objects.create(
        id_multa = nova_multa,
        **dados_item_multa
    )

    return nova_multa


@login_required
def criar_pagamento(request):
    usuario = request.user
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    status = request.GET.get('status')

    if status:
        if status == 'approved':
            Multas.objects.filter(id_usuario=request.user, status='PENDENTE').update(status='PAGO')


    # 1️⃣ Busca todos os empréstimos do usuário
    emprestimos = Emprestimos.objects.filter(id_user=usuario)
    print("Usuário:", usuario.username)
    print("Total de empréstimos:", emprestimos.count())

    for emprestimo in emprestimos:
        print(f"> Verificando empréstimo {emprestimo.id} - status: {emprestimo.status}")
        print("  - is_atrasado():", emprestimo.is_atrasado())
        print("  - calcular_multa():", emprestimo.calcular_multa())

        if emprestimo.is_atrasado():
            print("  ⚠️ Está atrasado! Verificando se já tem multa...")
            if not Multas.objects.filter(id_emprestimo=emprestimo).exists():
                print("  🧾 Criando nova multa...")
                emitir_multa(emprestimo)
            else:
                print("  🔄 Já existe multa, pulando...")

    multas_pendentes = Multas.objects.filter(id_usuario=usuario, status='PENDENTE')
    print("Multas pendentes encontradas:", multas_pendentes.count())
    
    itens_pagamento = []

    for multa in multas_pendentes:
        if multa.valor_multa:
            itens_pagamento.append({
                'id': f'ATRASO-{multa.pk}',
                'title': f'{multa.id_emprestimo.id_livro.nome}',
                'quantity': 1,
                "currency_id": "BRL",
                'unit_price': float(multa.valor_multa)
            })

    print(len(itens_pagamento))
    
    if len(itens_pagamento) > 0:
        pagamento_data = {
            'items': itens_pagamento,
            'back_urls': {
                'success': 'https://underbred-adriana-formally.ngrok-free.dev/user/multas/',
                'failure': 'https://underbred-adriana-formally.ngrok-free.dev/user/multas/',
                'pending': 'https://underbred-adriana-formally.ngrok-free.dev/user/multas/',
            },
            'auto_return': 'approved',
            "external_reference": f"MULTA-{usuario.id}"
        }

        preference = sdk.preference().create(pagamento_data)
        response_data = preference.get('response', {})
        print("Resposta do Mercado Pago:", response_data)

        preference_id = response_data.get('id')

        for multa in multas_pendentes:
            multa.preference_id = preference_id
            multa.save()

        link_pagamento = response_data.get('sandbox_init_point')
        print(link_pagamento)

        # ✅ Se o Mercado Pago retornou erro, não tente redirecionar
        if not link_pagamento or not isinstance(link_pagamento, str):
            return HttpResponse(f"Erro ao criar pagamento:<br><pre>{response_data}</pre>", status=400)
        
        context = {
            'link_pagamento': link_pagamento,
            'itens_pagamento': itens_pagamento,
        }

        return render(request, 'user/multas.html', context)
    
    else:
        return render(request, 'user/multas.html')