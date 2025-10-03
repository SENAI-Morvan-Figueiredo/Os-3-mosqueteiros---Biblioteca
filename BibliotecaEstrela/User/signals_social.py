from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_social_login)
def link_to_existing_user(sender, request, sociallogin, **kwargs):
    """
    Se o e-mail do social login já existe no banco, associa a social account
    ao usuário existente.
    """

    email = sociallogin.account.extra_data.get('email')

    if not email:
        return

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return
    
    sociallogin.connect(request, user)