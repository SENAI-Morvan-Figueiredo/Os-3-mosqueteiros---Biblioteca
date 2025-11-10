from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, tela_perfil, complete_signup, historico_perfil, notificacoes_perfil, atualizar_notif


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('cadastro/', register, name='user_register'),
    path('tela_perfil/', tela_perfil, name='tela_perfil'),
    path('notificacoes/', notificacoes_perfil, name='notificacoes_perfil'),
    path('atualizar_notif/<int:notif>/<str:tipo>/', atualizar_notif, name='atualizar_notif'),
    path('historico_perfil/', historico_perfil, name='historico_perfil'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/user/login'), name='logout'),
    path('completar_cadastro/', complete_signup, name='complete_signup'),
]