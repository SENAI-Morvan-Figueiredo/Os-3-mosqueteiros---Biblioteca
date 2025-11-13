from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    telefone = forms.CharField()
    cpf = forms.CharField()

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefone', 'cpf']
    

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
