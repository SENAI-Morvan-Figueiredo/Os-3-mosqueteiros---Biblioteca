from django.db import models

# Create your models here.

class Generos(models.Model):
    nome_genero = models.CharField()

class Livros(models.Model):
    nome = models.CharField()
    autor = models.CharField()
    editora = models.CharField()
    descricao = models.TextField()
    data_publicacao = models.DateField()
    imagem = models.ImageField(null=True)
    status = models.CharField()

class Livros_Generos(models.Model):
    id_livros = models.ForeignKey(Livros, on_delete=models.CASCADE)
    id_genero = models.ForeignKey(Generos, on_delete=models.CASCADE)