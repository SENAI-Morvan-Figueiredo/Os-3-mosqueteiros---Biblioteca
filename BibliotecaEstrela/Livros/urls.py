from django.urls import path
from .views import *

from Biblioteca.views import criar_emprestimo, criar_reserva

urlpatterns = [
    path('AdicionarLivro/', AdicionarLivro, name='adicionar_livro'),
    path('AdicionarCategoria/', AdicionarCategoria, name='adicionar_categoria'),
    path('livro/<str:busca>/', buscar_livro, name='busca_nome'),
    path('livro/<int:pk>/detalhes', LivroDetalhes.as_view(), name='livro_detalhes'),
    path('livro/<int:id_livro>/<int:id_user>/emprestimo', criar_emprestimo, name='criar_emprestimos'),
    path('livro/<int:id_livro>/<int:id_user>/reserva', criar_reserva, name='criar_reserva'),
    path('livro/confirmação', tela_confirmar, name='tela_confirmacao'),
    path("", Livros_view, name="livros"),
]