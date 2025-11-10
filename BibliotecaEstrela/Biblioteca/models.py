from django.db import models
from User.models import Usuario
from Livros.models import Livros

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

class Notificacoes(models.Model):
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensagem = models.CharField(max_length=150)
    lido = models.BooleanField("Marca uma notificação como lida/não lida")
    data = models.DateField(auto_now_add=True)

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