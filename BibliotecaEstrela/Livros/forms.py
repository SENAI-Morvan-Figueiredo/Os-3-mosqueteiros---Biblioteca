from django import forms
from .models import Livros, Generos, Livros_Generos

class GenerosForm(forms.ModelForm):
    class Meta:
        model = Generos
        fields = ['nome_genero']
        widgets = {
            'nome_genero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da categoria...'
            })
        }

class LivrosForm(forms.ModelForm):
    class Meta:
        model = Livros
        fields = ['nome', 'autor', 'editora', 'descricao', 'data_publicacao', 'status', 'imagem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editora': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'data_publicacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=[('disponivel','Disponível'), ('emprestado','Emprestado')]),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

class LivrosGenerosForm(forms.ModelForm):
    class Meta:
        model = Livros_Generos
        fields = ['id_genero']  # só o gênero
        labels = {
            'id_genero': 'Gênero',   # <-- aqui troca o texto do form
        }
        widgets = {
            'id_genero': forms.Select(attrs={'class': 'form-select'})
        }