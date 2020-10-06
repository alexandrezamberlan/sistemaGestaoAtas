from django import forms
from django.db import models

from usuario.models import Usuario

from .models import Curso


class CursoForm(forms.ModelForm):
    coordenador = forms.ModelChoiceField(label='Coordenador *', queryset=Usuario.professores.all())
    

    class Meta:
        model = Curso
        fields = ['nome','area', 'coordenador', 'email', 'is_active']
    
