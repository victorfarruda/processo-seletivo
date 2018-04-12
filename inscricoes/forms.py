from django import forms

from .models import Inscricao

from cidades.models import Cidade
from cursos.models import Curso

class InscricaoForm(forms.ModelForm):
    cidade_curso = forms.ModelChoiceField(queryset=Cidade.objects.all(), label='Cidade', widget=forms.Select(attrs={'class': 'form-control'}))
    curso = forms.ModelChoiceField(empty_label='---------',queryset=Curso.objects.all(), label='Curso', widget=forms.Select(attrs={'class': 'form-control'}))
    necessidade_esp = forms.CharField(required=False, label='Necessidade Especial',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Necessidade Especial'}))
    local_prova = forms.ModelChoiceField(queryset=Cidade.objects.all(), label='Local da Prova', widget=forms.Select(attrs={'class': 'form-control'}))
    curso_hidden = forms.CharField(label='', widget=forms.HiddenInput(attrs={'id':'curso_hidden'}))

    class Meta:
        model = Inscricao
        exclude = ['candidato']
