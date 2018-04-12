from django import forms

from .models import Perfil, Usuario


class PerfilForm(forms.ModelForm):
    nome = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    sobrenome = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}))
    data_nasc = forms.DateField(input_formats=['%d/%m/%Y'], label='Data de Nascimento',
                                widget=forms.DateInput(
                                    attrs={'class': 'form-control data', 'placeholder': 'Data de Nascimento'}))
    telefone = forms.CharField(label='Telefone',
                             widget=forms.TextInput(attrs={'class': 'form-control celular', 'placeholder': 'Telefone'}))
    rg = forms.CharField(label='RG', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RG'}))
    cpf = forms.CharField(label='CPF', widget=forms.TextInput(attrs={'class': 'form-control cpf', 'placeholder': 'CPF'}))

    class Meta:
        model = Perfil
        exclude = ['endereco']

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.fields['rg'].error_messages['required'] = 'O campo RG é obrigatório.'
        self.fields['rg'].error_messages['unique'] = 'Este número de RG já foi utilizado.'
        self.fields['cpf'].error_messages['required'] = 'O campo CPF é obrigatório.'
        self.fields['cpf'].error_messages['unique'] = 'Este número de CPF já foi utilizado.'
        self.fields['data_nasc'].error_messages['invalid'] = 'Insira uma data válida.'


class UsuarioForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}))
    password_confirm = forms.CharField(label='Confirme Senha',
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme Senha'}))

    class Meta:
        model = Usuario
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['email'].error_messages['unique'] = 'Este endereço de E-mail já foi utilizado.'

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Senhas não conferem!")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password_confirm"])
        if commit:
            user.save()
        return user

