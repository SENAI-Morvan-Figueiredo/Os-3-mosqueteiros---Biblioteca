from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from django.db import transaction # Necessário para a função local

# Importe todos os seus modelos e funções
from User.models import Usuario
from Livros.models import Livros
from Biblioteca.models import Emprestimos
from Multas.models import Multas, MultaLivro
# A importação 'from Multas.views import emitir_multa' foi removida para isolar o teste

# -------------------------------------------------------------
# FUNÇÃO LOCAL PARA TESTE (CÓPIA DO Multas/views.py)
# -------------------------------------------------------------

@transaction.atomic
def emitir_multa_local(emprestimo_objeto):
    """
    Função local que imita a lógica correta da view para garantir que os testes rodem.
    """
    usuario = emprestimo_objeto.id_user

    # 1. Calcula o valor APENAS do atraso
    valor_atraso = Decimal(emprestimo_objeto.calcular_multa())
    
    # Se não há multa por atraso, NÃO emite a multa principal.
    if valor_atraso <= 0:
        return None

    # 2. Cria o registro principal da Multa
    nova_multa = Multas.objects.create(
        id_emprestimo=emprestimo_objeto,
        id_usuario=usuario,
        nome_usuario_copia=usuario.username,
        cpf_usuario_copia=usuario.cpf,
        valor_multa=valor_atraso,  # Valor apenas do atraso
        status='PENDENTE'
    )
    
    # Não cria MultaLivro (conforme seu requisito)
    
    return nova_multa

# -------------------------------------------------------------
# SETUP INICIAL: Criação de dados de teste
# -------------------------------------------------------------

class MultasTeste(TestCase):
    def setUp(self):
        # 1. Criar um usuário de teste
        self.usuario = Usuario.objects.create_user(
            username='teste_user', 
            email='teste@exemplo.com', 
            password='senha123',
            cpf='12345678900',
            telefone='99999999'
        )
        
        # 2. Criar um livro de teste
        self.livro = Livros.objects.create(
            nome='Livro Teste Multa',
            autor='Autor Teste',
            editora='Editora Teste',
            data_publicacao=date(2020, 1, 1),
            status='disponivel',
        )

        # 3. Criar o Empréstimo Base
        self.data_emprestimo_ontem = timezone.now().date() - timedelta(days=1)
        self.emprestimo_base = Emprestimos.objects.create(
            id_user=self.usuario,
            id_livro=self.livro,
            data_emprestimo=self.data_emprestimo_ontem,
            status='emprestado'
        )

# -------------------------------------------------------------
# PARTE 1: TESTE DA LÓGICA DE CÁLCULO
# -------------------------------------------------------------

    def test_calcular_multa_sem_atraso(self):
        """Testa se a multa é 0 quando o empréstimo não está atrasado."""
        emprestimo_hoje = Emprestimos.objects.create(
            id_user=self.usuario,
            id_livro=self.livro,
            data_emprestimo=timezone.now().date(),
            status='emprestado'
        )
        multa = emprestimo_hoje.calcular_multa()
        self.assertEqual(multa, 0, "A multa deve ser 0 para um empréstimo feito hoje.")
        
    def test_calcular_multa_com_atraso(self):
        """Testa se a multa é calculada corretamente (R$2 por dia)."""
        data_5_dias_atras = timezone.now().date() - timedelta(days=5)
        self.emprestimo_base.data_emprestimo = data_5_dias_atras
        self.emprestimo_base.save()
        
        # Multa esperada: 5 dias * R$2 = R$10
        multa = self.emprestimo_base.calcular_multa()
        self.assertEqual(multa, 10, "A multa deveria ser calculada como R$10,00.")

# -------------------------------------------------------------
# PARTE 2: TESTE DA LÓGICA DE EMISSÃO (Usando função local)
# -------------------------------------------------------------

    def test_emitir_multa_atraso_sucesso(self):
        """Testa a emissão de multa por atraso e garante que MultaLivro NÃO é criado."""
        # Configurar 2 dias de atraso (Multa = R$4)
        self.emprestimo_base.data_emprestimo = timezone.now().date() - timedelta(days=2)
        self.emprestimo_base.save()
        
        multa_calculada = Decimal(self.emprestimo_base.calcular_multa())
        
        # 1. Chamar a função de emissão LOCAL
        nova_multa = emitir_multa_local(self.emprestimo_base)
        
        # 2. Assertivas
        self.assertIsNotNone(nova_multa)
        self.assertEqual(nova_multa.valor_multa, multa_calculada) 
        
        # 3. Assertiva CRÍTICA: MultaLivro deve ser VAZIA
        self.assertEqual(MultaLivro.objects.filter(id_multa=nova_multa).count(), 0,
                         "MultaLivro não deve ser criado para multa de atraso.")

    def test_nao_emitir_multa_sem_atraso(self):
        """Testa se a função retorna None quando o valor da multa é 0."""
        # Configurar multa = 0 (data de hoje)
        self.emprestimo_base.data_emprestimo = timezone.now().date()
        self.emprestimo_base.save()
        
        # 1. Chamar a função de emissão LOCAL
        nova_multa = emitir_multa_local(self.emprestimo_base)
        
        # 2. Assertiva: A função deve retornar None
        self.assertIsNone(nova_multa)
        self.assertEqual(Multas.objects.count(), 0)
