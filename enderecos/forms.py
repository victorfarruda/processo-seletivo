from django import forms

from .models import Endereco

class EnderecoForm(forms.ModelForm):
    cep = forms.CharField(label='CEP', widget=forms.TextInput(attrs={'class': 'form-control text cep', 'placeholder': 'CEP'}))
    rua = forms.CharField(label='Rua', widget=forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Rua'}))
    numero = forms.CharField(label='Número', widget=forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Número'}))
    complemento = forms.CharField(required=False, label='Complemento', widget=forms.TextInput(
        attrs={'class': 'form-control text', 'placeholder': 'Complemento'}))
    bairro = forms.CharField(label='Bairro', widget=forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Bairro'}))
    cidade = forms.CharField(label='Cidade', widget=forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Cidade'}))
    estado = forms.CharField(label='Estado', widget=forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Estado'}))

    class Meta:
        model = Endereco
        fields = '__all__'
