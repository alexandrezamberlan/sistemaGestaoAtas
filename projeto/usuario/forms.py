from django import forms
from .models import Usuario
from curso.models import Curso

class UsuarioRegisterForm(forms.ModelForm):
    TIPOS_USUARIOS = (
        ('PROFESSOR', 'Professor' ),
        ('SECRETÁRIA', 'Secretária' ),
    )
    
    tipo = forms.ChoiceField(label='Tipo',choices=TIPOS_USUARIOS)
    nome = forms.CharField(label='Nome completo *' , help_text='Campo obrigatório como todos os que tiverem *' )
    matricula = forms.CharField(label='Matrícula *', max_length=15, required = True)
    curso = forms.ModelMultipleChoiceField(label='Curso vinculado ', help_text='Caso você pertença a mais de um curso, deixe em branco', queryset=Curso.objects.all())
    email = forms.EmailField(label= 'Email *', max_length=100)
    password = forms.CharField(label= "Senha", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['tipo','nome','matricula','curso','email','password']