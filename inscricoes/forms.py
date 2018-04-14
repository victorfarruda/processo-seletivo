from django import forms

from .models import Inscricao
from .choices import MODALIDADE_CHOICES

from cidades.models import Cidade
from cursos.models import Curso


class InscricaoForm(forms.ModelForm):
    cidade_curso = forms.ModelChoiceField(queryset=Cidade.objects.all(), label='Cidade', widget=forms.Select(attrs={'class': 'form-control'}))
    curso = forms.ModelChoiceField(empty_label='---------',queryset=Curso.objects.all(), label='Curso', widget=forms.Select(attrs={'class': 'form-control'}))
    necessidade_esp = forms.CharField(required=False, label='Necessidade Especial',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Necessidade Especial'}))
    local_prova = forms.ModelChoiceField(queryset=Cidade.objects.all(), label='Local da Prova', widget=forms.Select(attrs={'class': 'form-control'}))
    modalidade = forms.ChoiceField(choices=MODALIDADE_CHOICES, label='Modalidade',
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    curso_hidden = forms.CharField(label='', widget=forms.HiddenInput(attrs={'id':'curso_hidden'}))

    class Meta:
        model = Inscricao
        exclude = ['candidato']


class MinhaInscricaoForm(forms.ModelForm):
    cidade_curso = forms.ModelChoiceField(queryset=Cidade.objects.all(), label='Cidade',
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    curso = forms.ModelChoiceField(empty_label='---------', queryset=Curso.objects.all(), label='Curso',
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    necessidade_esp = forms.CharField(required=False, label='Necessidade Especial',
                                      widget=forms.TextInput(
                                          attrs={'class': 'form-control', 'placeholder': 'Necessidade Especial'}))
    local_prova = forms.ModelChoiceField(queryset=Cidade.objects.all(), label='Local da Prova',
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    modalidade = forms.ChoiceField(label='Modalidade',
                                        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Inscricao
        exclude = ['candidato']

    def __init__(self, *args, **kwargs):
        super(MinhaInscricaoForm, self).__init__(*args, **kwargs)
        self.fields['cidade_curso'].queryset = Cidade.objects.filter(id=self.instance.cidade_curso.id)
        self.fields['curso'].queryset = Curso.objects.filter(id=self.instance.curso.id)
        self.fields['local_prova'].queryset = Cidade.objects.filter(id=self.instance.local_prova.id)
        selecionado = tuple(i for i in MODALIDADE_CHOICES if self.instance.modalidade in i)
        self.fields['modalidade'].choices = selecionado
