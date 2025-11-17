from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from django.utils.text import slugify
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Usuario
from .utils import gerar_avatar_inicial

@receiver(user_signed_up)
def populate_user_data(request, user, sociallogin=None, **kwargs):
    print("⚡ user_signed_up disparado para:", user.email)

    # Garante que o usuário tenha um username único
    if not user.username:
        base_username = user.email.split('@')[0]
        unique_suffix = uuid.uuid4().hex[:6]
        user.username = slugify(f"{base_username}-{unique_suffix}")

    # Garante que CPF e telefone existam (mesmo vazios)
    if not getattr(user, 'telefone', None):
        user.telefone = ''
    if not getattr(user, 'cpf', None):
        user.cpf = ''

    user.save()


@receiver(user_logged_in)
def redirect_after_social_login(request, user, **kwargs):
    # Marca na sessão que o usuário precisa completar o cadastro
    if not user.cpf or not user.telefone:
        request.session['must_complete_profile'] = True

@receiver(post_save, sender=Usuario)
def criar_foto_perfil(sender, instance, created, **kwargs):
    if created:
        primeira_letra = instance.first_name[0].upper() if instance.first_name else instance.username[0].upper()

        imagem = gerar_avatar_inicial(primeira_letra)
        instance.imagem.save(f'{instance.username}_avatar.png', imagem)