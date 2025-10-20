from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, tela_perfil, historico_perfil

from Multas.views import minhas_multas

urlpatterns = [
    path('cadastro/', register, name='user_register'),
    path('tela_perfil/', tela_perfil, name='tela_perfil'),
    path('historico_perfil/', historico_perfil, name='historico_perfil'),

    path('multas/', minhas_multas, name='multas'),


    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/user/login'), name='logout'),
]