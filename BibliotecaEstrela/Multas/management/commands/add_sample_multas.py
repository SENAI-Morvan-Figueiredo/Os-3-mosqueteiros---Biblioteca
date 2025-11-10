from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from Multas.models import Multas, MultaLivro
from User.models import Usuario
from Biblioteca.models import Emprestimos
from Livros.models import Livros


class Command(BaseCommand):
    help = 'Cria multas de teste com datas antigas (para desenvolvimento)'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=3, help='Quantidade de multas a criar')
        parser.add_argument('--start-days', type=int, default=30, help='Dias atrás do primeiro registro')
        parser.add_argument('--step', type=int, default=1, help='Incremento de dias entre registros')
        parser.add_argument('--user', type=int, help='ID do usuário (opcional)')
        parser.add_argument('--emprestimo', type=int, help='ID do empréstimo a vincular (opcional)')
        parser.add_argument('--valor-por-dia', type=float, default=1.0, help='Valor por dia de atraso (padrão 1.0)')
        parser.add_argument('--valor', type=float, help='Valor fixo da multa (sobrepõe cálculo por dia)')

    def handle(self, *args, **options):
        count = options['count']
        start_days = options['start_days']
        step = options['step']
        user_id = options.get('user')
        emprestimo_id = options.get('emprestimo')
        valor_por_dia = Decimal(str(options.get('valor_por_dia', 1.0)))
        valor_fixo = options.get('valor')

        hoje = timezone.now().date()

        # Escolhe usuário
        usuario = None
        if user_id:
            usuario = Usuario.objects.filter(id=user_id).first()
            if not usuario:
                self.stdout.write(self.style.ERROR(f'Usuário com id={user_id} não encontrado'))
                return
        else:
            usuario = Usuario.objects.first()
            if not usuario:
                self.stdout.write(self.style.ERROR('Nenhum usuário encontrado no banco. Crie um usuário primeiro.'))
                return

        # Escolhe livro/emprestimo
        emprestimo = None
        livro = None
        if emprestimo_id:
            emprestimo = Emprestimos.objects.filter(id=emprestimo_id).first()
            if not emprestimo:
                self.stdout.write(self.style.ERROR(f'Emprestimo com id={emprestimo_id} não encontrado'))
                return
            livro = emprestimo.id_livro
        else:
            emprestimo = Emprestimos.objects.first()
            livro = Livros.objects.first()
            if not emprestimo or not livro:
                self.stdout.write(self.style.ERROR('Nenhum empréstimo/livro encontrado no banco. Crie registros primeiro.'))
                return

        created = []
        for i in range(count):
            dias_atraso_total = start_days + i * step
            data_emissao = hoje - timedelta(days=dias_atraso_total)

            # calcula dias que ultrapassam o prazo padrão de 21 dias
            dias_de_atraso = max(0, dias_atraso_total - 21)

            if valor_fixo is not None:
                valor = Decimal(str(valor_fixo))
            else:
                valor = Decimal(dias_de_atraso) * valor_por_dia

            multa = Multas.objects.create(
                id_emprestimo=emprestimo,
                id_usuario=usuario,
                nome_usuario_copia=str(usuario.username),
                cpf_usuario_copia=getattr(usuario, 'cpf', ''),
                valor_multa=valor,
            )

            # Atualiza data_emissao (auto_now_add) via update
            Multas.objects.filter(id=multa.id).update(data_emissao=data_emissao)

            # cria MultaLivro para referência
            MultaLivro.objects.create(
                id_multa=multa,
                id_livro=livro,
                titulo_livro_copia=getattr(livro, 'nome', ''),
                autor_livro_copia=getattr(livro, 'autor', ''),
                quantidade=1,
                valor_unitario=valor,
            )

            created.append(multa)
            self.stdout.write(self.style.SUCCESS(f'Criada multa id={multa.id} data_emissao={data_emissao} valor={valor}'))

        self.stdout.write(self.style.SUCCESS(f'Concluído: {len(created)} multas criadas.'))
