from django.shortcuts import render
from django.http import request

from .forms import InscricaoForm
from enderecos.forms import EnderecoForm
from contas.forms import PerfilForm, UsuarioForm


def inscricao(request):
    endereco = EnderecoForm(request.POST or None)
    perfil = PerfilForm(request.POST or None)
    inscricao = InscricaoForm(request.POST or None)
    usuario = UsuarioForm(request.POST or None)
    if request.method == 'POST':
        print(usuario.errors)
        print(endereco.errors)
        print(inscricao.errors)
        print(perfil.errors)
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
            # return redirect('')
    context = {
        'titulo': 'Inscrição - ',
        'form_endereco': endereco,
        'form_usuario': usuario,
        'form_perfil': perfil,
        'form_inscricao': inscricao,
    }
    return render(request, 'inscricoes/inscricao.html', context)