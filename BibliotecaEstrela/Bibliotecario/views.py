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
    
    # Lógica de busca
    query = request.GET.get('q')
    if query:
        emprestimos = Emprestimos.objects.filter(
            Q(status="Disponível para retirar") | Q(status="Retirado")
        ).filter(
            Q(id_user__username__icontains=query) |
            Q(id_livro__nome__icontains=query) |
            Q(status__icontains=query)
        )
        reservas = Reserva.objects.filter(status="Em espera").filter(
            Q(id_user__username__icontains=query) |
            Q(id_livro__nome__icontains=query)
        )
    else:
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
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

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

    # Lógica de busca para livros
    query = request.GET.get('q')
    if query:
        livros = Livros.objects.filter(
            Q(nome__icontains=query) |
            Q(autor__icontains=query) |
            Q(editora__icontains=query)
        )
    else:
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
    
    # --- Importação das Multas ---
    from Multas.models import Multas
    
    # --- Listas para as tabelas ---
    # Mostrar empréstimos atrasados dinamicamente (propriedade calculada) OU status explícito 'Atrasado'
    todos_emprestimos = Emprestimos.objects.all().order_by('data_emprestimo')
    emprestimos_atrasados = [e for e in todos_emprestimos if getattr(e, 'esta_atrasado', False) or (getattr(e, 'status', '') == 'Atrasado')]
    
    emprestimos_cancelados = Emprestimos.objects.filter(
        status="Cancelado"
    ).order_by('-data_emprestimo') # Ordena do mais novo para o mais antigo

    # Pedidos de extensão pendentes
    from Biblioteca.models import Pedidos_extensao
    pedidos_extensao = Pedidos_extensao.objects.filter(status__in=['Pendente', 'pendente']).select_related('id_emprestimo__id_user', 'id_emprestimo__id_livro')

    # Multas pendentes e pagas
    multas_pendentes = Multas.objects.filter(status='PENDENTE').select_related('id_usuario', 'id_emprestimo__id_livro').order_by('-data_emissao')
    multas_pagas = Multas.objects.filter(status='PAGO').select_related('id_usuario', 'id_emprestimo__id_livro').order_by('-data_emissao')[:10]  # Últimas 10

    # Calcular valor total das multas pendentes
    from django.db.models import Sum
    valor_total_multas = multas_pendentes.aggregate(total=Sum('valor_multa'))['total'] or 0

    # Lógica de busca
    query = request.GET.get('q')
    if query:
        # Filtrar tabelas com base na pesquisa
        emprestimos_atrasados = [e for e in todos_emprestimos if (getattr(e, 'esta_atrasado', False) or (getattr(e, 'status', '') == 'Atrasado')) and (
            query.lower() in e.id_user.username.lower() or 
            query.lower() in e.id_livro.nome.lower() or 
            query.lower() in e.status.lower()
        )]
        
        emprestimos_cancelados = Emprestimos.objects.filter(
            status="Cancelado"
        ).filter(
            Q(id_user__username__icontains=query) |
            Q(id_livro__nome__icontains=query)
        ).order_by('-data_emprestimo')
        
        pedidos_extensao = pedidos_extensao.filter(
            Q(id_emprestimo__id_user__username__icontains=query) |
            Q(id_emprestimo__id_livro__nome__icontains=query)
        )
        
        multas_pendentes = multas_pendentes.filter(
            Q(nome_usuario_copia__icontains=query) |
            Q(cpf_usuario_copia__icontains=query)
        )

    context = {
        # Para os cards de estatística
        "livros": livros_stats,
        "usuarios": usuarios_stats,
        "reservas": reservas_stats, # Usando a contagem de reservas ativas
        "emprestimos_ativos": emprestimos_ativos, # Usando a contagem de ativos
        
        # Para as tabelas
        "emprestimos_atrasados": emprestimos_atrasados,
        "emprestimos_cancelados": emprestimos_cancelados,
        "pedidos_extensao": pedidos_extensao,
        "multas_pendentes": multas_pendentes,
        "multas_pagas": multas_pagas,
        "valor_total_multas": valor_total_multas,
    }
    return render(request, 'dashboard.html', context)


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
        
        emprestimos_para_atrasar = Emprestimos.objects.filter(
            status="Retirado", # Se está "Retirado"
            data_emprestimo__lt=data_limite_atraso # E foi emprestado há mais de 14 dias
        )
        
        # .update() é mais rápido para atualizar muitos objetos
        count_atrasados = emprestimos_para_atrasar.update(
            status="Atrasado" # <-- NOVO STATUS
        )

        # Envia uma mensagem de sucesso para o template
        messages.success(request, f"Verificação concluída: {count_cancelados} empréstimos cancelados e {count_atrasados} marcados como atrasados.")

    # Redireciona de volta para a página principal de empréstimos
    return redirect("Bibliotecario:emprestimos_atuais")


@login_required
def aprovar_extensao(request, pedido_id):
    # Apenas usuários administradores podem aprovar
    if not request.user.is_superuser:
        return HttpResponseForbidden('Permissão negada')

    from Biblioteca.models import Pedidos_extensao
    pedido = Pedidos_extensao.objects.filter(id=pedido_id).select_related('id_emprestimo').first()
    if not pedido:
        return HttpResponse('Pedido não encontrado', status=404)

    emprestimo = pedido.id_emprestimo
    # concede 7 dias adicionais
    emprestimo.prazo_extra = (getattr(emprestimo, 'prazo_extra', 0) or 0) + 7
    emprestimo.save()

    pedido.status = 'Aprovado'
    pedido.save()

    return redirect('Bibliotecario:dashboard')


@login_required
def recusar_extensao(request, pedido_id):
    # Apenas usuários administradores podem recusar
    if not request.user.is_superuser:
        return HttpResponseForbidden('Permissão negada')

    from Biblioteca.models import Pedidos_extensao
    pedido = Pedidos_extensao.objects.filter(id=pedido_id).first()
    if not pedido:
        return HttpResponse('Pedido não encontrado', status=404)

    pedido.status = 'Recusado'
    pedido.save()

    return redirect('Bibliotecario:dashboard')

########
# VIEWS PARA PESQUISAS
########

# view para pesquisa de usuário:

# View para ver detalhes de um usuário
def ver_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        emprestimos_usuario = Emprestimos.objects.filter(id_user=usuario).order_by('-data_emprestimo')
        reservas_usuario = Reserva.objects.filter(id_user=usuario).order_by('-data_reserva')
        
        # Importar multas se necessário
        from Multas.models import Multas
        multas_usuario = Multas.objects.filter(id_usuario=usuario).order_by('-data_emissao')
        
        context = {
            'usuario': usuario,
            'emprestimos_usuario': emprestimos_usuario,
            'reservas_usuario': reservas_usuario,
            'multas_usuario': multas_usuario,
        }
        return render(request, 'usuario_detalhes.html', context)
    except Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("Bibliotecario:usuarios")

# View para deletar usuário
def deletar_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        
        # Verificar se o usuário tem empréstimos ativos antes de deletar
        emprestimos_ativos = Emprestimos.objects.filter(
            id_user=usuario, 
            status__in=['Disponível para retirar', 'Retirado', 'Emprestado']
        )
        
        # Verificar também reservas ativas
        from Biblioteca.models import Reserva
        reservas_ativas = Reserva.objects.filter(
            id_user=usuario,
            status='Em espera'
        )
        
        # Verificar multas pendentes
        from Multas.models import Multas
        multas_pendentes = Multas.objects.filter(
            id_usuario=usuario,
            status='PENDENTE'
        )
        
        # Lista de impedimentos
        impedimentos = []
        if emprestimos_ativos.exists():
            impedimentos.append(f"{emprestimos_ativos.count()} empréstimo(s) ativo(s)")
        if reservas_ativas.exists():
            impedimentos.append(f"{reservas_ativas.count()} reserva(s) ativa(s)")
        if multas_pendentes.exists():
            impedimentos.append(f"{multas_pendentes.count()} multa(s) pendente(s)")
            
        if impedimentos:
            messages.error(request, f"Não é possível deletar o usuário {usuario.username}. Ele possui: {', '.join(impedimentos)}.")
        else:
            nome_usuario = usuario.username
            usuario.delete()
            messages.success(request, f"Usuário {nome_usuario} foi deletado com sucesso.")
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
    except Exception as e:
        messages.error(request, f"Erro ao deletar usuário: {str(e)}")
    
    return redirect("Bibliotecario:usuarios")

# View para editar livro
def editar_livro(request, livro_id):
    try:
        livro = Livros.objects.get(id=livro_id)
        
        if request.method == "POST":
            form = LivrosForm(request.POST, request.FILES, instance=livro)
            if form.is_valid():
                form.save()
                messages.success(request, f"Livro '{livro.nome}' foi atualizado com sucesso.")
                return redirect("Bibliotecario:livros_adm")
        else:
            form = LivrosForm(instance=livro)
        
        context = {
            'form': form,
            'livro': livro,
            'editando': True,
        }
        return render(request, 'editar_livro.html', context)
        
    except Livros.DoesNotExist:
        messages.error(request, "Livro não encontrado.")
        return redirect("Bibliotecario:livros_adm")

# View para deletar livro
def deletar_livro(request, livro_id):
    try:
        livro = Livros.objects.get(id=livro_id)
        
        # Verificar se o livro tem empréstimos ativos antes de deletar
        emprestimos_ativos = Emprestimos.objects.filter(
            id_livro=livro, 
            status__in=['Disponível para retirar', 'Retirado']
        )
        
        if emprestimos_ativos.exists():
            messages.error(request, f"Não é possível deletar o livro '{livro.nome}'. Ele possui empréstimos ativos.")
        else:
            nome_livro = livro.nome
            livro.delete()
            messages.success(request, f"Livro '{nome_livro}' foi deletado com sucesso.")
        
    except Livros.DoesNotExist:
        messages.error(request, "Livro não encontrado.")
    
    return redirect("Bibliotecario:livros_adm")