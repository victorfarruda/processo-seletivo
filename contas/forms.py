from django import forms

from .models import Perfil, Usuario


class PerfilForm(forms.ModelForm):
    nome = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Nome'}))
    sobrenome = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'Sobrenome'}))
    data_nasc = forms.DateField(input_formats=['%d/%m/%Y'], label='Data de Nascimento',
                                widget=forms.DateInput(
                                    attrs={'class': 'form-control text data', 'placeholder': 'Data de Nascimento'}))
    telefone = forms.CharField(label='Telefone',
                             widget=forms.TextInput(attrs={'class': 'form-control text celular', 'placeholder': 'Telefone'}))
    rg = forms.CharField(label='RG', widget=forms.TextInput(attrs={'class': 'form-control text', 'placeholder': 'RG'}))
    cpf = forms.CharField(label='CPF', widget=forms.TextInput(attrs={'class': 'form-control text cpf', 'placeholder': 'CPF'}))

    class Meta:
        model = Perfil
        exclude = ['endereco']

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.fields['data_nasc'].error_messages['invalid'] = 'Insira uma data válida.'

    def clean_rg(self):
        rg = self.cleaned_data.get('rg')
        if rg is None:
            raise forms.ValidationError("O campo RG é obrigatório.")
        if self.instance.id:
            rg_antigo = Perfil.objects.get(id__exact=self.instance.id).rg
            if not self.instance.usuario.is_admin and rg != rg_antigo:
                raise forms.ValidationError("Você não tem permissão para editar este campo.")
        existe = Perfil.objects.filter(rg__iexact=rg).exclude(id__exact=self.instance.id).exists()
        if existe:
            raise forms.ValidationError("Este número de RG já foi utilizado.")
        return rg

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf is None:
            raise forms.ValidationError("O campo CPF é obrigatório.")
        if self.instance.id:
            cpf_antigo = Perfil.objects.get(id__exact=self.instance.id).cpf
            if not self.instance.usuario.is_admin and cpf != cpf_antigo:
                raise forms.ValidationError("Você não tem permissão para editar este campo.")
        existe = Perfil.objects.filter(cpf__iexact=cpf).exclude(id__exact=self.instance.id).exists()
        if existe:
            raise forms.ValidationError("Este número de CPF já foi utilizado.")
        return cpf


class UsuarioForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control text', 'placeholder': 'E-mail'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control text', 'placeholder': 'Senha'}))
    password_confirm = forms.CharField(label='Confirme Senha',
                               widget=forms.PasswordInput(attrs={'class': 'form-control text', 'placeholder': 'Confirme Senha'}))

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


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control text', 'placeholder': 'E-mail'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control text', 'placeholder': 'Senha'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        usuario = Usuario.objects.filter(email__iexact=email).exists()
        if not usuario:
            raise forms.ValidationError("Email não encontrado!")
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        usuario_existe = Usuario.objects.filter(email__iexact=email).exists()
        if usuario_existe:
            usuario = Usuario.objects.get(email__iexact=email)
            if not usuario.check_password(password):
                raise forms.ValidationError("Senha Inválida!")
        return password

