from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    telefone = forms.CharField()
    cpf = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirme sua senha"

        self.fields['password2'].help_text = "Digite a mesma senha novamente para confirmação."

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Digite seu nome'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Digite seu email'
        })
        self.fields['telefone'].widget.attrs.update({
            'placeholder': 'Digite seu telefone'
        })
        self.fields['cpf'].widget.attrs.update({
            'placeholder': 'Digite seu cpf'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Digite sua senha'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirme sua senha'
        })

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefone', 'cpf', 'password1', 'password2']
        labels = {
            'username': 'Nome*',
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Alterar labels
        self.fields['username'].label = "Email"
        self.fields['password'].label = "Senha"

        # Alterar placeholders
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Digite seu email'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Digite sua senha'
        })

class UserUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'cpf', 'telefone', 'imagem']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('new_password')

        if password:
            user.set_password(password)
        if commit:
            user.save()

        return user
    
class CompleteSignupForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['telefone', 'cpf']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['telefone'].required = True
            self.fields['cpf'].required = True
            
class UserUpdateImageForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['imagem']
        widgets = {
            'imagem': forms.FileInput(attrs={
                'accept': 'image/*',  # opcional: limita a imagens
            }),
        }

class SetPasswordFormPTBR(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    new_password2 = forms.CharField(
        label="Confirmar nova senha",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )