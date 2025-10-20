from django.db import models
from django.urls import reverse
import uuid
from datetime import date, timedelta
from Biblioteca.models import Emprestimos

# Create your models here.

class Payment(models.Model):
    emprestimo = models.ForeignKey(Emprestimos, on_delete=models.CASCADE, related_name='payments', blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=10, choices=[('pix','Pix'),('card','Cartão')], default='pix')
    status = models.CharField(max_length=10, choices=[('pending','Pendente'),('completed','Concluído'),('failed','Falhou')], default='pending')
    pix_code = models.TextField(blank=True, null=True)
    card_last4 = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)