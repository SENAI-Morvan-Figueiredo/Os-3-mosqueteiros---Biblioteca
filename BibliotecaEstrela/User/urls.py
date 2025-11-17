from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, tela_perfil, complete_signup, historico_perfil


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('cadastro/', register, name='user_register'),
    path('tela_perfil/', tela_perfil, name='tela_perfil'),
    path('historico_perfil/', historico_perfil, name='historico_perfil'),
    path('login/', LoginView.as_view(template_name='User/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/User/login'), name='logout'),
    path('completar_cadastro/', complete_signup, name='complete_signup'),
]