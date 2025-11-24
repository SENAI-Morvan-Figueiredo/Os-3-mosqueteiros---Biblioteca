from django.db import models

# Create your models here.

class Generos(models.Model):
    nome_genero = models.CharField()
    def __str__(self):
        return self.nome_genero

class Livros(models.Model):
    nome = models.CharField()
    autor = models.CharField()
    editora = models.CharField()
    descricao = models.TextField()
    data_publicacao = models.DateField()
    imagem = models.ImageField(upload_to="capas/", null=True, blank=True)
    status = models.CharField()

    def __str__(self):
        return self.nome


class Livros_Generos(models.Model):
    id_livros = models.ForeignKey(Livros, on_delete=models.CASCADE)
    id_genero = models.ForeignKey(Generos, on_delete=models.CASCADE)