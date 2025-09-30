from django.urls import path
from .views import *

urlpatterns = [
    path('AdicionarLivro/', AdicionarLivro, name='adicionar_livro'),
    path('AdicionarCategoria/', AdicionarCategoria, name='adicionar_categoria'),
    path('livro/<int:pk>/', LivroDetalhes.as_view(), name='livro_detalhes'),
    path("", Livros_view, name="livros"),
]