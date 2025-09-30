from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    telefone = models.CharField()
    cpf = models.CharField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['username', 'telefone', 'cpf']

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)

    def __str__(self):
        return self.email