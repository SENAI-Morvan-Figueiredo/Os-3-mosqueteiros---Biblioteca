# User/middleware.py
from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from django.conf import settings

class CompleteProfileMiddleware:
    """
    Redireciona o usuário para 'complete_signup' (nome da url) se a
    sessão marcar que ele deve completar o perfil (must_complete_profile)
    e se telefone/cpf estiverem faltando.
    """
    def __init__(self, get_response):
        self.get_response = get_response

        # Prefixos que NÃO devem ser interceptados (static, media, admin, allauth callbacks)
        self.exempt_prefixes = (
            getattr(settings, "STATIC_URL", "/static/"),
            getattr(settings, "MEDIA_URL", "/media/"),
            '/admin/',
            '/accounts/',   # endpoints do allauth (login/callback/etc.) - não queremos quebrar o fluxo
            '/favicon.ico',
        )

    def __call__(self, request):
        # Só age para usuários autenticados
        if request.user.is_authenticated:
            # Se a sessão indicou que o usuário precisa completar o perfil
            if request.session.get('must_complete_profile', False):
                path = request.path

                # Se a rota atual for a própria tela de completar cadastro, limpa a flag e passa
                try:
                    complete_path = reverse('complete_signup')
                except NoReverseMatch:
                    complete_path = None

                if complete_path and path == complete_path:
                    # permite acessar a tela de completar cadastro; limpa a flag para evitar loop
                    request.session.pop('must_complete_profile', None)
                    return self.get_response(request)

                # Não redireciona se a requisição for para uma rota isenta
                for prefix in self.exempt_prefixes:
                    if prefix and path.startswith(prefix):
                        return self.get_response(request)

                # Se os dados estiverem realmente faltando, redireciona
                cpf = getattr(request.user, 'cpf', None)
                telefone = getattr(request.user, 'telefone', None)
                if not cpf or not telefone:
                    # evita redirecionar em chamadas AJAX
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return self.get_response(request)
                    return redirect('complete_signup')

        return self.get_response(request)
