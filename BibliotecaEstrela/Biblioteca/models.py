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