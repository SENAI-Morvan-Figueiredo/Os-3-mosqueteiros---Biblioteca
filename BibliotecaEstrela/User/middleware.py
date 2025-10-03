# User/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class CompleteProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se o usuário está autenticado
        if request.user.is_authenticated:
            # Campos obrigatórios
            required_fields = ['cpf', 'telefone', 'email']
            incomplete = any(not getattr(request.user, field, None) for field in required_fields)

            # Evita loop infinito: não redirecionar se já estiver na página de completar perfil
            if incomplete and request.path != reverse('complete_profile'):
                return redirect('complete_profile')

        response = self.get_response(request)
        return response
