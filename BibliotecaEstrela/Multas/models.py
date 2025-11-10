from django.db import models
from django.urls import reverse
import uuid

from User.models import Usuario
from Livros.models import Livros
from Biblioteca.models import Emprestimos

from datetime import date, timedelta

# Create your models here.
class Multas(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pagamento pendente'),
        ('PAGO', 'Pagamento concluído') 
    ]
    
    id_emprestimo = models.ForeignKey(Emprestimos, on_delete=models.SET_NULL, null=True) 
    id_usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    
    nome_usuario_copia = models.CharField(max_length=255, help_text="Nome do usuário no momento da emissão")
    cpf_usuario_copia = models.CharField(max_length=14, help_text="CPF do usuário no momento da emissão")
    
    valor_multa = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissao = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')

    livros_a_pagar = models.ManyToManyField(Livros, through='MultaLivro')

    def __str__(self):
        return self.id_emprestimo
    
class MultaLivro(models.Model):
    id_multa = models.ForeignKey(Multas, on_delete=models.CASCADE,) 
    id_livro = models.ForeignKey(Livros, on_delete=models.SET_NULL,null=True)

    titulo_livro_copia = models.CharField(max_length=255)
    autor_livro_copia = models.CharField(max_length=255)

    quantidade = models.PositiveIntegerField(default=1)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.titulo_livro_copia

    class Meta:
        unique_together = ('id_multa', 'id_livro')