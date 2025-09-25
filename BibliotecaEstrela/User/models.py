from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario(AbstractUser):
    email = models.EmailField()
    telefone = models.CharField()

    REQUIRED_FIELDS=['email', 'telefone']