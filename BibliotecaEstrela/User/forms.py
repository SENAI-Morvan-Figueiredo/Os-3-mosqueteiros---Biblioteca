from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    telefone = forms.CharField()
    cpf = forms.CharField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefone', 'cpf', 'password', 'password2']