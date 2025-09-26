from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, tela_vazia

urlpatterns = [
    path('cadastro/', register, name='user_register'),
    path('tela_perfil/', tela_vazia, name='tela_perfil'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/user'), name='logout'),
]