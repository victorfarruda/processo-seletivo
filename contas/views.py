from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.db.models import Q
from django.http import (
    request,
    Http404,
)
from django.shortcuts import render
from django.shortcuts import redirect

from enderecos.forms import EnderecoForm
from inscricoes.forms import (
    RecursoForm,
    RespostaRecursoForm,
)
from .forms import (
    LoginForm,
    PerfilForm,
)


def login_page(request):
    if request.user.is_authenticated():
        return redirect('inicio')
    login_form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')
    context = {
        'login': login_form,
    }
    return render(request, 'contas/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


def meus_dados(request):
    usuario = request.user
    endereco = EnderecoForm(request.POST or None, instance=usuario.endereco)
    if endereco.is_valid():
        endereco.save()
    perfil = PerfilForm(request.POST or None, instance=usuario.perfil)
    if perfil.is_valid():
        perfil.save()
    context = {
        'form_perfil': perfil,
        'form_endereco': endereco,
    }
    return render(request, 'contas/meus_dados.html', context)


def recursos(request):
    inscricao = request.user.inscricao
    recursos = inscricao.recurso_set.all()
    context = {
        'recursos': recursos,
    }
    return render(request, 'inscricoes/recursos.html', context)


def recurso_inscricao(request, tipo):
    inscricao = request.user.inscricao
    recurso = inscricao.recurso_set.all().filter(
        Q(recurso__isnull=True) | Q(recurso__exact=''),
        Q(status__exact='3'),
        Q(tipo__exact=tipo),
    ).first()
    if recurso is None:
        raise Http404('Página não encontrada')
    form_recurso = RecursoForm(request.POST or None, instance=recurso)
    recurso_tipo = 'Socioeconômico' if tipo == 'socio' else 'Reserva de Vagas'
    if request.method == 'POST':
        if form_recurso.is_valid():
            form_recurso.save()
            return redirect('recursos')
    context = {
        'form_recurso': form_recurso,
        'recurso_tipo': recurso_tipo
    }
    return render(request, 'inscricoes/recurso.html', context)


def recurso_resultado(request, tipo):
    inscricao = request.user.inscricao
    recurso = inscricao.recurso_set.all().filter(
        Q(tipo__exact=tipo),
    ).first()
    if recurso is None:
        raise Http404('Página não encontrada')
    form_recurso = RespostaRecursoForm(request.POST or None, instance=recurso)
    recurso_tipo = 'Socioeconômico' if tipo == 'socio' else 'Reserva de Vagas'
    context = {
        'form_recurso': form_recurso,
        'recurso_tipo': recurso_tipo
    }
    return render(request, 'inscricoes/recurso.html', context)