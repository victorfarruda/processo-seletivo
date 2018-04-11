from django.shortcuts import render
from django.http import request
from django.http import JsonResponse
from django.http import Http404

from cidades.models import Cidade


def get_cursos(request, id):
    if request.method == 'POST':
        cursos = Cidade.objects.get(id=id).curso.all()
        lista = [
            {'curso': curso.curso, 'id': curso.id,} for curso in cursos
        ]
        return JsonResponse(lista, safe=False)
    else:
        raise Http404