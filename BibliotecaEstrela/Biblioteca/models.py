from django.db import models
from User.models import Usuario
from Livros.models import Livros

# Create your models here.

class Emprestimos(models.Model):
    id_user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_livro = models.ForeignKey(Livros, on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    status = models.CharField()

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