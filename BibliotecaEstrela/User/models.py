from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario(AbstractUser):
    email = models.EmailField()
    telefone = models.CharField()
    cpf = models.CharField()
    imagem = models.ImageField(upload_to='imagem_perfil', blank=True, null=True)

    REQUIRED_FIELDS=['email', 'telefone', 'cpf']