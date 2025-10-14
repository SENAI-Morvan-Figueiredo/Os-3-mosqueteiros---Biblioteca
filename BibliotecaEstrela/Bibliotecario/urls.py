from django.urls import path
from .views import *
app_name = 'Bibliotecario'
urlpatterns = [
    path("", teste, name="teste"),
    path("/livros", livros, name="livros_adm"),
    path("/emprestimos_atuais", emprestimos_atuais, name="emprestimos_atuais")
]