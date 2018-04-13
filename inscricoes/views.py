from django.contrib.auth import login
from django.http import request
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from .utils import criar_codigo_barras

from .forms import (
    InscricaoForm,
    MinhaInscricaoForm
)
from enderecos.forms import EnderecoForm
from contas.forms import (
    PerfilForm,
    UsuarioForm
)

from .models import Inscricao

def inscricao_page(request):
    if request.user.is_authenticated():
        return redirect('inicio')
    endereco = EnderecoForm(request.POST or None)
    perfil = PerfilForm(request.POST or None)
    inscricao = InscricaoForm(request.POST or None)
    usuario = UsuarioForm(request.POST or None)
    if request.method == 'POST':
        if endereco.is_valid() and perfil.is_valid() and inscricao.is_valid() and usuario.is_valid():
            endereco_obj = endereco.save()
            perfil_obj = perfil.save()
            usuario_obj = usuario.save(commit=False)
            usuario_obj.endereco = endereco_obj
            usuario_obj.perfil = perfil_obj
            usuario_obj.nome = perfil_obj.nome
            usuario_obj.save()
            inscricao_obj = inscricao.save(commit=False)
            inscricao_obj.candidato = usuario_obj
            inscricao_obj.save()
            login(request, usuario_obj)
            return redirect('login')
    context = {
        'titulo': 'Inscrição - ',
        'form_endereco': endereco,
        'form_usuario': usuario,
        'form_perfil': perfil,
        'form_inscricao': inscricao,
    }
    return render(request, 'inscricoes/inscricao.html', context)


def minha_inscricao(request):
    usuario = request.user
    inscricao = Inscricao.objects.get(candidato__exact=usuario.id)
    if inscricao:
        inscricao_form = MinhaInscricaoForm(request.POST or None, instance=inscricao)
    context = {
        'form_inscricao': inscricao_form,
    }
    return render(request, 'inscricoes/minha_inscricao.html', context)


def comprovante_inscricao(request):
    usuario = request.user
    inscricao = Inscricao.objects.get(candidato__exact=usuario.id)

    context = {
        'inscricao': inscricao,
    }
    return render(request, 'inscricoes/comprovante.html', context)


def codigo_barras(request, text):
    codigo_barra = criar_codigo_barras(text)
    binaryStuff = codigo_barra.asString('gif')
    return HttpResponse(binaryStuff, 'image/gif')