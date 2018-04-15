from django import forms

from .models import (
    Inscricao,
    SocioEconomico,
    Recurso,
)
from .choices import (
    INSCRICAO_CHOICES,
    MODALIDADE_CHOICES,
    RECURSO_CHOICES,
    QUESTAO_01,
    QUESTAO_02,
    QUESTAO_03,
    QUESTAO_04,
    QUESTAO_05,
    QUESTAO_06,
    QUESTAO_07,
    QUESTAO_08,
    QUESTAO_09,
    QUESTAO_10,
    QUESTAO_11,
    QUESTAO_12,
)

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


class SocioEconomicoForm(forms.ModelForm):
    pai = forms.CharField(label='Nome do Pai', widget=forms.TextInput(attrs={'class': 'form-control'}))
    mae = forms.CharField(label='Nome da Mãe', widget=forms.TextInput(attrs={'class': 'form-control'}))
    questao1 = forms.ChoiceField(label='01 - Renda familiar per capta:', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_01)
    questao2 = forms.ChoiceField(label='02 - Escola em que cursou o Ensino Médio:', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_02)
    questao3 = forms.ChoiceField(label='03 - Escola em que fez integralmente o ensino fundamental:', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_03)
    questao4 = forms.ChoiceField(label='04 - Escola/instituição em que fez ou está fazendo cursinho pré-vestibular:', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_04)
    questao5 = forms.ChoiceField(label='05 - O candidato ou algum membro da família participa de programa social do governo federal?', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_05)
    questao6 = forms.ChoiceField(label='06 - Situação civil do candidato:', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_06)
    questao7 = forms.ChoiceField(label='07- Se o candidato é solteiro e não mora com a família:', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_07)
    questao8 = forms.ChoiceField(label='08 - Situação da casa em que reside o grupo familiar:', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_08)
    questao9 = forms.ChoiceField(label='09 - Além do próprio candidato, quantos membros do grupo familiar vão se inscrever no programa socioeconômico para concessão de desconto/isenção:', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_09)
    questao10 = forms.ChoiceField(label='10 - O candidato ou membro do grupo familiar utiliza medicamento de uso contínuo?', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_10)
    questao11 = forms.ChoiceField(label='11 - Participa do programa detarifa social da COPASA?', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_11)
    questao12 = forms.ChoiceField(label='12 - Participa do programa de tarifa social da CEMIG?', widget=forms.RadioSelect(attrs={'class': 'form-check-input'}), choices=QUESTAO_12)

    class Meta:
        model = SocioEconomico
        exclude = ['inscricao']


class ReservaForm(forms.ModelForm):
    status = forms.ChoiceField(label='Selecione:', widget=forms.RadioSelect(), choices=RECURSO_CHOICES)
    motivo_indeferimento = forms.CharField(label='Informe o motivo do Indeferimento:', widget=forms.Textarea(), required=False)

    class Meta:
        model = Recurso
        fields = ['status', 'motivo_indeferimento', ]

    def clean_motivo_indeferimento(self):
        status = self.cleaned_data.get('status')
        motivo_indeferimento = self.cleaned_data.get('motivo_indeferimento')
        if status == '2':  # Deferido
            return motivo_indeferimento
        if status == '3':  # Indeferido
            if motivo_indeferimento == '':
                raise forms.ValidationError('Este campo não pode ser vazio.')
        return motivo_indeferimento