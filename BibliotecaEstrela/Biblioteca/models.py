from django.db import models
from User.models import Usuario
from Livros.models import Livros
from datetime import date, timedelta

# Create your models here.

class Emprestimos(models.Model):
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_livro = models.ForeignKey(Livros, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    status = models.CharField()
    @property
    def esta_atrasado(self):
        """Retorna True se o empréstimo estiver atrasado (mais de 21 dias desde a data_emprestimo)."""
        from datetime import date, timedelta
        try:
            hoje = date.today()
            limite = self.data_emprestimo + timedelta(days=21)
            if self.status in ('Devolvido', 'Cancelado', 'Atrasado'):
                return False
            return hoje > limite
        except Exception:
            return False

    PRAZO_DIAS = 1
    
    def is_atrasado(self):
        """
        Retorna True se o empréstimo estiver em atraso:
        - status deve ser de que o livro foi retirado/emprestado (não 'Disponível para retirar')
        - e já passaram mais que PRAZO_DIAS desde data_emprestimo
        """

        status_val = (self.status or '').strip().lower()

        estados_emprestado = ('retirado', 'emprestado')

        if status_val not in estados_emprestado:
            return False
        
        dias = (date.today() - self.data_emprestimo).days

        return dias > self.PRAZO_DIAS
    
    def calcular_multa(self):
        """
        Calcula o valor da multa apenas se o empréstimo estiver atrasado.
        """
        # Se não estiver atrasado, multa = 0
        if not self.is_atrasado():
            return 0

        dias_emprestados = (date.today() - self.data_emprestimo).days
        dias_atraso = dias_emprestados - self.PRAZO_DIAS
        multa_total = dias_atraso * 2  # R$ 2,00 por dia de atraso
        return multa_total

    def get_dados_multa_livro(self):
        livro = self.id_livro

        return {
            'id_livro': livro,
            'titulo_livro_copia': livro.nome,
            'autor_livro_copia': livro.autor,
            'quantidade': 1,
            'valor_unitario': 0.00
        }


    @property
    def dias_atraso(self):
        """Retorna a quantidade de dias de atraso além do prazo de 21 dias.

        Retorna 0 se não estiver atrasado ou em caso de erro.
        """
        from datetime import date, timedelta
        try:
            hoje = date.today()
            limite = self.data_emprestimo + timedelta(days=21)
            if self.status in ('Devolvido', 'Cancelado'):
                return 0
            dias = (hoje - limite).days
            return dias if dias > 0 else 0
        except Exception:
            return 0

    @property
    def data_vencimento(self):
        """Data prevista de entrega (data_emprestimo + 21 dias)."""
        from datetime import timedelta
        try:
            return self.data_emprestimo + timedelta(days=21)
        except Exception:
            return None

    @property
    def dias_restantes(self):
        """Retorna os dias restantes até a data de vencimento. 0 se já venceu ou erro."""
        from datetime import date
        try:
            if not self.data_vencimento:
                return 0
            dias = (self.data_vencimento - date.today()).days
            return dias if dias > 0 else 0
        except Exception:
            return 0

    @property
    def data_retirada_limite(self):
        """Data limite para o usuário retirar o livro (quando status é 'Disponível para retirar'). 7 dias a partir de data_emprestimo."""
        from datetime import timedelta
        try:
            return self.data_emprestimo + timedelta(days=7)
        except Exception:
            return None

    @property
    def dias_para_retirada(self):
        """Dias restantes para retirar o livro (apenas relevante quando o status é 'Disponível para retirar')."""
        from datetime import date
        try:
            limite = self.data_retirada_limite
            if not limite:
                return 0
            dias = (limite - date.today()).days
            return dias if dias > 0 else 0
        except Exception:
            return 0

class Notificacoes(models.Model):
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensagem = models.CharField(max_length=150)
    lido = models.BooleanField("Marca uma notificação como lida/não lida")
    data = models.DateField(auto_now_add=True)
class Reserva(models.Model):
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_livro = models.ForeignKey(Livros, on_delete=models.CASCADE)
    data_reserva = models.DateField(auto_now_add=True)
    status = models.CharField()

class Avaliacoes(models.Model):
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_livro = models.ForeignKey(Livros, on_delete=models.CASCADE)
    nota = models.SmallIntegerField()
    titulo = models.CharField(max_length=50)
    texto = models.TextField()

class Pedidos_extensao(models.Model):
    id_emprestimo = models.ForeignKey(Emprestimos, on_delete=models.CASCADE)
    status = models.CharField()