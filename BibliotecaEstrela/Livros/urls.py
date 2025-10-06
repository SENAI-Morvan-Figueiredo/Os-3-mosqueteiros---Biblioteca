from django.urls import path
from . import views
app_name = 'Livros'
urlpatterns = [
    path('AdicionarLivro/', views.AdicionarLivro, name='AdicionarLivro'),
    path('AdicionarCategoria/', views.AdicionarCategoria, name='adicionar_categoria'),
    path("", views.Livros_view, name="livros"),
]