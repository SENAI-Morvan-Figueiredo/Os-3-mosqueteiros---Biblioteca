from django.shortcuts import render, redirect, HttpResponse
from Livros.models import Livros, Generos, Livros_Generos
from User.models import Usuario
from Biblioteca.models import Emprestimos, Reserva
from .forms import GenerosForm, LivrosForm, LivrosGenerosForm
from django.views.generic import DetailView
from django.db.models import Q
import datetime

# view para tela inicial (todo: trocar nomes)
def teste(request):
    livros = Livros.objects.all()
    usuarios = Usuario.objects.all()
    emprestimos = Emprestimos.objects.all()
    context = {
        "livros": livros,
        "usuarios": usuarios,
        "emprestimos": emprestimos,
    }
    return render(request, 'index.html', context)

# view para empréstimos atuais
def emprestimos_atuais(request):
    livros = Livros.objects.all()
    usuarios = Usuario.objects.all()
    # importante: para futuramente filtrar, troca o do empréstiimppara aqueles que "possue"
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # todo: adicionar uma variável para unicamente o card a esquerda (não gerar conflito)
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    emprestimos = Emprestimos.objects.filter(
    Q(status="Disponível para retirar") | Q(status="Retirado")
    )
    reservas = Reserva.objects.filter(status="Em espera")
    context = {
        "livros": livros,
        "usuarios": usuarios,
        "emprestimos":  emprestimos,
        "reservas": reservas,
    }
    return render(request, 'emprestimos_atuais.html', context)

from django.contrib import messages

# atualizar status emprestimo

"""
!!!!!!!!!!!!!!!!!!!!!
IMPORTANTE:
Tome cuidado com o "disponivel" ou "indisponivel", digamos que são as "palavras chave", não altera se não estiverenm nestas condições.
!!!!!!!!!!!!!!!!!!!!!
"""
def atualizar_status(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("status_"):
                emprestimo_id = key.split("_")[1]
                novo_status = value

                # Atualiza o status do empréstimo
                emprestimo = Emprestimos.objects.filter(id=emprestimo_id).first()
                if emprestimo:
                    emprestimo.status = novo_status
                    emprestimo.save()

                    # Atualiza o status do livro (models do livro)
                    livro = emprestimo.id_livro
                    if novo_status == "Retirado":
                        livro.status = "Indisponivel"
                        livro.save()
                    elif novo_status == "Devolvido":
                        livro.status = "disponivel"
                        livro.save()

        messages.success(request, "Status dos empréstimos atualizados com sucesso!")
    return redirect("Bibliotecario:emprestimos_atuais")


from django.utils import timezone
from decimal import Decimal
from Multas.models import Multas, MultaLivro

# atualiza reserva (muda de reserva para empréstimo)
def atualizar_status_reservas(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("status_"):
                reserva_id = key.split("_")[1]
                novo_status = value

                # Atualiza a reserva
                reserva = Reserva.objects.filter(id=reserva_id).first()
                if reserva:
                    reserva.status = novo_status
                    reserva.save()

                    # Se for Finalizado, cria um empréstimo automaticamente
                    if novo_status == "Finalizado":
                        Emprestimos.objects.create(
                            id_user=reserva.id_user,
                            id_livro=reserva.id_livro,
                            data_emprestimo=timezone.now(),
                            status="Disponível para retirar"
                        )
        messages.success(request, "Status das reservas atualizadas com sucesso!")
    return redirect("Bibliotecario:emprestimos_atuais")



# view para empréstimos todos (pesquisa/histórico)
def emprestimos_historico(request):
    # 1. Pega os dados para os cards de estatística (sempre todos)
    livros_stats = Livros.objects.all()
    usuarios_stats = Usuario.objects.all()
    emprestimos_stats = Emprestimos.objects.all() # Usado no card da esquerda
    
    # 2. Pega o termo da busca
    query = request.GET.get('q')

    if query:
        # 3. Se houver busca, filtra as DUAS listas
        # Busca por nome do usuário (no model Usuario) ou nome do livro (no model Livros)
        emprestimos_lista = Emprestimos.objects.filter(
            Q(id_user__username__icontains=query) | 
            Q(id_livro__nome__icontains=query)
        )
        
        reservas_lista = Reserva.objects.filter(
            Q(id_user__username__icontains=query) | 
            Q(id_livro__nome__icontains=query)
        )
    else:
        # 4. Se não houver busca, pega todos os registros
        emprestimos_lista = Emprestimos.objects.all()
        reservas_lista = Reserva.objects.all()

    context = {
        # Variáveis para os cards de estatística
        "livros": livros_stats,
        "usuarios": usuarios_stats,
        "emprestimos": emprestimos_stats, # Para o card
        
        # Variáveis NOVAS para as tabelas (filtradas ou não)
        "emprestimos_tabela": emprestimos_lista,
        "reservas_tabela": reservas_lista,
    }
    return render(request, 'emprestimos_historico.html', context)

# view para todos os usuários (pesquisa/histórico)
def usuarios(request):
    # Pega os dados para os cards de estatística (sempre todos)
    livros_stats = Livros.objects.all()
    usuarios_stats = Usuario.objects.all()
    emprestimos_stats = Emprestimos.objects.all()
    
    # --- Lógica da Busca ---
    # Pega o parâmetro 'q' da URL (ex: /usuarios/?q=teo)
    query = request.GET.get('q')

    if query:
        # Se houver uma query, filtra a lista de usuários
        # Busca por nome, email ou CPF que contenham o texto da query
        usuarios_lista = Usuario.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(cpf__icontains=query)
        )
    else:
        # Se não houver query, mostra todos os usuários
        usuarios_lista = Usuario.objects.all()
    # --- Fim da Lógica da Busca ---

    context = {
        # Dados para os cards da esquerda (estatísticas)
        "livros": livros_stats,
        "usuarios": usuarios_stats, # 'usuarios' para o card de estatísticas
        "emprestimos": emprestimos_stats,
        
        # 'usuarios_lista' para a tabela (filtrada ou não)
        "usuarios_lista_tabela": usuarios_lista, 
    }
    return render(request, 'usuarios.html', context)
# view para livro para adm:
def livros(request):
    if request.method == "POST":
        livro_form = LivrosForm(request.POST, request.FILES)
        categoria_form = GenerosForm(request.POST)

        if livro_form.is_valid():
            livro = livro_form.save()  # salva o livro primeiro

            # pega os gêneros enviados
            generos_ids = request.POST.getlist("id_genero")
            for genero_id in generos_ids:
                Livros_Generos.objects.create(id_livros=livro, id_genero_id=genero_id)

            return redirect("Bibliotecario:livros_adm")
    
        if categoria_form.is_valid():
            categoria_form.save()
            return redirect("Bibliotecario:livros_adm")
    else:
        livro_form = LivrosForm()
        genero_form = LivrosGenerosForm()
        form = GenerosForm()

    livros = Livros.objects.all()
    generos = Generos.objects.all()
    usuarios = Usuario.objects.all()
    emprestimos = Emprestimos.objects.all()
    context = {
        "livros": livros,
        "generos": generos,
        "usuarios": usuarios,
        "emprestimos": emprestimos,
        "livro_form": livro_form,
        "genero_form": genero_form,
        "form": form,
    }
    return render(request, 'adm_livros.html', context)


# view para dashboard adm

# !!!
# A base é esta, falta filtrar e adicionar as funcionalidades de multa, etc
# !!!
def dashboard(request):
    # --- Estatísticas para os cards ---
    livros_stats = Livros.objects.all()
    usuarios_stats = Usuario.objects.all()
    
    # Filtra reservas ativas (use o status correto do seu model)
    reservas_stats = Reserva.objects.filter(status="Em espera") 
    
    # Filtra empréstimos ativos (não inclui devolvidos, cancelados ou atrasados)
    emprestimos_ativos = Emprestimos.objects.filter(
        Q(status="Disponível para retirar") | Q(status="Retirado")
    )
    
    # --- Listas para as novas tabelas ---
    # Mostrar empréstimos atrasados dinamicamente (propriedade calculada) OU status explícito 'Atrasado'
    todos_emprestimos = Emprestimos.objects.all().order_by('data_emprestimo')
    emprestimos_atrasados = [e for e in todos_emprestimos if getattr(e, 'esta_atrasado', False) or (getattr(e, 'status', '') == 'Atrasado')]
    
    emprestimos_cancelados = Emprestimos.objects.filter(
        status="Cancelado"
    ).order_by('-data_emprestimo') # Ordena do mais novo para o mais antigo
    # Multas (para exibir no dashboard do bibliotecário/admin)
    multas = Multas.objects.all().order_by('-data_emissao')

    context = {
        # Para os cards de estatística
        "livros": livros_stats,
        "usuarios": usuarios_stats,
        "reservas": reservas_stats, # Usando a contagem de reservas ativas
        "emprestimos_ativos": emprestimos_ativos, # Usando a contagem de ativos
        
        # Para as novas tabelas
        "emprestimos_atrasados": emprestimos_atrasados,
        "emprestimos_cancelados": emprestimos_cancelados,
        "multas": multas,
    }
    return render(request, 'dashboard.html', context)


def atualizar_status_multas(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('multa_'):
                multa_id = key.split('_')[1]
                novo_status = value
                multa = Multas.objects.filter(id=multa_id).first()
                if multa:
                    multa.status = novo_status
                    multa.save()
        messages.success(request, 'Status das multas atualizados com sucesso!')
    return redirect('Bibliotecario:dashboard')


def verificar_pendencias(request):
    """
    Esta view é chamada pelo botão manual "Verificar Pendências".
    Ela executa a lógica de cancelamento e atraso.
    """
    
    # Apenas POST requests devem modificar dados
    if request.method == "POST":
        hoje = timezone.now().date()
        
        count_cancelados = 0
        count_atrasados = 0

        # --- Lógica 1: Cancelar Empréstimos não retirados ---
        # "Disponível para retirar" e passou de 7 dias
        data_limite_cancelar = hoje - datetime.timedelta(days=7)
        
        # Encontra os empréstimos que estão "Disponível para retirar"
        # e foram criados há mais de 7 dias
        emprestimos_para_cancelar = Emprestimos.objects.filter(
            status="Disponível para retirar",
            data_emprestimo__lt=data_limite_cancelar # __lt = "less than" (menor que)
        )
        
        for emprestimo in emprestimos_para_cancelar:
            emprestimo.status = "Cancelado"  # <-- NOVO STATUS
            emprestimo.save()
            
            # Importante: Devolve o livro para a prateleira virtual
            livro = emprestimo.id_livro
            livro.status = "disponivel"  # Use o status que seu Model Livros entende
            livro.save()
            count_cancelados += 1

        # --- Lógica 2: Marcar Empréstimos Atrasados ---
        # "Retirado" e passou de 14 dias (2 semanas)
        data_limite_atraso = hoje - datetime.timedelta(days=14)

        emprestimos_para_atrasar_qs = Emprestimos.objects.filter(
            status="Retirado", # Se está "Retirado"
            data_emprestimo__lt=data_limite_atraso # E foi emprestado há mais de 14 dias
        )

        emprestimos_para_atrasar = list(emprestimos_para_atrasar_qs)

        # Para cada empréstimo, marcar como Atrasado e criar/atualizar multa
        for emprestimo in emprestimos_para_atrasar:
            emprestimo.status = "Atrasado"
            emprestimo.save()

            # calcula dias de atraso a partir da propriedade do model
            dias = getattr(emprestimo, 'dias_atraso', 0)
            valor = Decimal(dias) * Decimal('1.00')

            # Atualiza ou cria multa associada
            multa = Multas.objects.filter(id_emprestimo=emprestimo).first()
            if multa:
                # só atualiza se estiver pendente
                if multa.status == 'PENDENTE':
                    multa.valor_multa = valor
                    multa.save()
            else:
                multa = Multas.objects.create(
                    id_emprestimo=emprestimo,
                    id_usuario=emprestimo.id_user,
                    nome_usuario_copia=str(emprestimo.id_user.username),
                    cpf_usuario_copia=getattr(emprestimo.id_user, 'cpf', ''),
                    valor_multa=valor,
                )
                # cria registro de livro vinculado
                MultaLivro.objects.create(
                    id_multa=multa,
                    id_livro=emprestimo.id_livro,
                    titulo_livro_copia=getattr(emprestimo.id_livro, 'nome', ''),
                    autor_livro_copia=getattr(emprestimo.id_livro, 'autor', ''),
                    quantidade=1,
                    valor_unitario=valor,
                )

        count_atrasados = len(emprestimos_para_atrasar)

        # Envia uma mensagem de sucesso para o template
        messages.success(request, f"Verificação concluída: {count_cancelados} empréstimos cancelados e {count_atrasados} marcados como atrasados.")

    # Redireciona de volta para a página principal de empréstimos
    return redirect("Bibliotecario:emprestimos_atuais")

########
# VIEWS PARA PESQUISAS
########

# view para pesquisa de usuário:
