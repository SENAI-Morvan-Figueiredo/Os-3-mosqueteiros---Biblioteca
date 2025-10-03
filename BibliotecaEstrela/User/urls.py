from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, tela_perfil, complete_profile

urlpatterns = [
    path('cadastro/', register, name='user_register'),
    path('tela_perfil/', tela_perfil, name='tela_perfil'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/user/login'), name='logout'),

    # Completar perfil (após login social)
    path('complete-profile/', complete_profile, name='complete_profile'),
]