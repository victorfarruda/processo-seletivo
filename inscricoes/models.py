from django.db import models

from cidades.models import Cidade
from cursos.models import Curso
from contas.models import Usuario


class Inscricao(models.Model):
    candidato       = models.OneToOneField(Usuario)
    cidade_curso    = models.OneToOneField(Cidade, related_name='cidade_curso')
    curso           = models.OneToOneField(Curso)
    local_prova     = models.ForeignKey(Cidade, related_name='local_prova')
    necessidade_esp = models.CharField(max_length=120, blank=True, null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' tes'