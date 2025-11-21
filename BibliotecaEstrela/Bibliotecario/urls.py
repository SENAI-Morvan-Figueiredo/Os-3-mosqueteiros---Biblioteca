from django.urls import path
from .views import *
app_name = 'Bibliotecario'
urlpatterns = [
    path("", teste, name="teste"),
    path("livros/", livros, name="livros_adm"),
    path("emprestimos_atuais/", emprestimos_atuais, name="emprestimos_atuais"),
    path("emprestimos_historico/", emprestimos_historico, name="emprestimos_historico"),
    path("usuarios/", usuarios, name="usuarios"),
    path("dashboard/", dashboard, name="dashboard"),
    path("emprestimos/atualizar_status/", atualizar_status, name="atualizar_status"),
    path("reservas/atualizar_status/", atualizar_status_reservas, name="atualizar_status_reservas"),
    path('verificar_pendencias/', verificar_pendencias, name='verificar_pendencias'),
    path('extensoes/aprovar/<int:pedido_id>/', aprovar_extensao, name='aprovar_extensao'),
    path('extensoes/recusar/<int:pedido_id>/', recusar_extensao, name='recusar_extensao'),
    path('usuario/<int:usuario_id>/', ver_usuario, name='ver_usuario'),
    path('usuario/<int:usuario_id>/deletar/', deletar_usuario, name='deletar_usuario'),
    path('livro/<int:livro_id>/editar/', editar_livro, name='editar_livro'),
    path('livro/<int:livro_id>/deletar/', deletar_livro, name='deletar_livro'),
    path('emprestimo/<int:emprestimo_id>/deletar/', deletar_emprestimo, name='deletar_emprestimo'),
    path('reserva/<int:reserva_id>/deletar/', deletar_reserva, name='deletar_reserva'),

]