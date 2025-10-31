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

    def calcular_multa(self):
        prazo = self.data_emprestimo + timedelta(days=0)  # prazo de devolução
        atraso = (date.today() - prazo).days
        return max(atraso * 2, 0)  # R$2 por dia, no mínimo 0

    def get_dados_multa_livro(self):
        livro = self.id_livro

        return {
            'id_livro': livro,
            'titulo_livro_copia': livro.nome,
            'autor_livro_copia': livro.autor,
            'quantidade': 1,
            'valor_unitario': 0.00
        }


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