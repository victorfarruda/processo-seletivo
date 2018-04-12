from django.contrib.auth import login
from django.http import request
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import InscricaoForm
from enderecos.forms import EnderecoForm
from contas.forms import PerfilForm, UsuarioForm


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