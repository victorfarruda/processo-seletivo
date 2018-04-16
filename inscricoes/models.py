from django.db import models
from django.db.models.signals import post_save

from cidades.models import Cidade
from cursos.models import Curso
from contas.models import Usuario

from .choices import (
    MODALIDADE_CHOICES,
    INSCRICAO_CHOICES,
    RECURSO_CHOICES,
    TIPO_RECURSO,
)


class Inscricao(models.Model):
    candidato = models.OneToOneField(Usuario)
    cidade_curso = models.ForeignKey(Cidade, related_name='cidade_curso')
    curso = models.ForeignKey(Curso)
    local_prova = models.ForeignKey(Cidade, related_name='local_prova')
    necessidade_esp = models.CharField(max_length=120, blank=True, null=True)
    modalidade = models.CharField(max_length=10, choices=MODALIDADE_CHOICES)
    reserva = models.CharField(max_length=2, editable=False, choices=INSCRICAO_CHOICES, null=True, blank=True)
    socio_economico = models.CharField(max_length=2, editable=False, choices=INSCRICAO_CHOICES, null=True, blank=True)
    valor = models.CharField(max_length=6, default='100,00')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.candidato.perfil.nome, self.candidato.perfil.sobrenome)


def post_save_reserva_receiver(sender, created, instance, *args, **kwargs):
    if created and instance.modalidade != 'universal':
        instance.reserva = '1'  # Inscrito
        instance.save()


post_save.connect(post_save_reserva_receiver, sender=Inscricao)


class SocioEconomico(models.Model):
    inscricao = models.OneToOneField(Inscricao)
    pai = models.CharField(max_length=120, null=True)
    mae = models.CharField(max_length=120, null=True)
    questao1 = models.CharField(max_length=10, null=True)
    questao2 = models.CharField(max_length=10, null=True)
    questao3 = models.CharField(max_length=10, null=True)
    questao4 = models.CharField(max_length=10, null=True)
    questao5 = models.CharField(max_length=10, null=True)
    questao6 = models.CharField(max_length=10, null=True)
    questao7 = models.CharField(max_length=10, null=True)
    questao8 = models.CharField(max_length=10, null=True)
    questao9 = models.CharField(max_length=10, null=True)
    questao10 = models.CharField(max_length=10, null=True)
    questao11 = models.CharField(max_length=10, null=True)
    questao12 = models.CharField(max_length=10, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.inscricao.candidato.perfil.nome, self.inscricao.candidato.perfil.sobrenome)


def post_save_socio_economico_receiver(sender, created, instance, *args, **kwargs):
    if created:
        inscricao_socio = instance.inscricao
        inscricao_socio.socio_economico = '1'  # Inscrito
        inscricao_socio.save()


post_save.connect(post_save_socio_economico_receiver, sender=SocioEconomico)


class Recurso(models.Model):
    inscricao = models.ForeignKey(Inscricao)
    status = models.CharField(max_length=120, choices=RECURSO_CHOICES)
    motivo_indeferimento = models.TextField()
    recurso = models.TextField(blank=True, null=True)
    resposta_recurso = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=120, choices=TIPO_RECURSO)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.inscricao.candidato.perfil.nome, self.inscricao.candidato.perfil.sobrenome)