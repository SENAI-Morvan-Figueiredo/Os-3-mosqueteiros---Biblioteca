from django.urls import path
from . import views

urlpatterns = [
    path('AdicionarLivro/', views.AdicionarLivro, name='adicionar_livro'),
    path('AdicionarCategoria/', views.AdicionarCategoria, name='adicionar_categoria'),
    path("", views.Livros_view, name="livros"),
]