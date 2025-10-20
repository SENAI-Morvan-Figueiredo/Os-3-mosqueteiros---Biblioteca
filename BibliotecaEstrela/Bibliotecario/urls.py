from django.urls import path
from .views import *
app_name = 'Bibliotecario'
urlpatterns = [
    path("", teste, name="teste"),
    path("/livros", livros, name="livros_adm"),
    path("/emprestimos_atuais", emprestimos_atuais, name="emprestimos_atuais"),
    path("/emprestimos_historico", emprestimos_historico, name="emprestimos_historico"),
    path("/usuarios", usuarios, name="usuarios"),
    path("/dashboard", dashboard, name="dashboard"),
    path("emprestimos/atualizar_status/", atualizar_status, name="atualizar_status"),
    path("reservas/atualizar_status/", atualizar_status_reservas, name="atualizar_status_reservas"),

]