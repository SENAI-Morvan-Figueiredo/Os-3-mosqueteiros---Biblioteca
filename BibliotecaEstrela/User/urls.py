from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, tela_perfil, complete_signup, historico_perfil, notificacoes_perfil, atualizar_notif
from django.contrib.auth import views as auth_views
from .forms import SetPasswordFormPTBR


from Multas.views import criar_pagamento

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('cadastro/', register, name='user_register'),
    path('tela_perfil/', tela_perfil, name='tela_perfil'),
    path('notificacoes/', notificacoes_perfil, name='notificacoes_perfil'),
    path('atualizar_notif/<int:notif>/<str:tipo>/', atualizar_notif, name='atualizar_notif'),
    path('historico_perfil/', historico_perfil, name='historico_perfil'),

    path('multas/', criar_pagamento, name='multas'),


    path('login/', LoginView.as_view(template_name='User/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/User/login'), name='logout'),
    path('completar_cadastro/', complete_signup, name='complete_signup'),

    path(
        'senha/reset/', auth_views.PasswordResetView.as_view(template_name='User/registration/email_reset_senha.html'), name='password_reset'
    ),

    # Recuperação de senha
path(
    'senha/reset/',
    auth_views.PasswordResetView.as_view(
        template_name='registration/email_reset_senha.html'
    ),
    name='password_reset'
),

path(
    'senha/reset/enviado/',
    auth_views.PasswordResetDoneView.as_view(
        template_name='registration/email_enviado.html'
    ),
    name='password_reset_done'
),

path(
    'senha/reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='User/registration/conteudo_email_retornado.html',
        form_class=SetPasswordFormPTBR,
        success_url=reverse_lazy('login')
    ),
    name='password_reset_confirm'
),

path(
    'senha/reset/feito/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/confirmar_reset_senha.html'
    ),
    name='password_reset_complete'
),
]