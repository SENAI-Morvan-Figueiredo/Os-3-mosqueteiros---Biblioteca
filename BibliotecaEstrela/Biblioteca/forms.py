from django import forms
from .models import Avaliacoes

class FormAval(forms.ModelForm):
    class Meta:
        model = Avaliacoes
        fields = ('nota', 'titulo' , 'texto')