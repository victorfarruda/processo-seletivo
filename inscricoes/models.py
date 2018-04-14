from django.db import models
from django.db.models.signals import post_save

from cidades.models import Cidade
from cursos.models import Curso
from contas.models import Usuario

from .choices import MODALIDADE_CHOICES


class Inscricao(models.Model):
    candidato = models.OneToOneField(Usuario)
    cidade_curso = models.ForeignKey(Cidade, related_name='cidade_curso')
    curso = models.ForeignKey(Curso)
    local_prova = models.ForeignKey(Cidade, related_name='local_prova')
    necessidade_esp = models.CharField(max_length=120, blank=True, null=True)
    modalidade = models.CharField(max_length=10, choices=MODALIDADE_CHOICES)
    reserva = models.NullBooleanField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.candidato.email


def post_save_reserva_receiver(sender, created, instance, *args, **kwargs):
    if created and instance.modalidade != 'universal':
        instance.reserva = False
        instance.save()


post_save.connect(post_save_reserva_receiver, sender=Inscricao)


class Socioeconomico(models.Model):
    inscricao = models.OneToOneField(Inscricao)
    pai = models.CharField(max_length=120, null=True)
    mae = models.CharField(max_length=120, null=True)
    questa1 = models.CharField(max_length=10, null=True)
    questa2 = models.CharField(max_length=10, null=True)
    questa3 = models.CharField(max_length=10, null=True)
    questa4 = models.CharField(max_length=10, null=True)
    questa5 = models.CharField(max_length=10, null=True)
    questa6 = models.CharField(max_length=10, null=True)
    questa7 = models.CharField(max_length=10, null=True)
    questa8 = models.CharField(max_length=10, null=True)
    questa9 = models.CharField(max_length=10, null=True)
    questa10 = models.CharField(max_length=10, null=True)
    questa11 = models.CharField(max_length=10, null=True)
    questa12 = models.CharField(max_length=10, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)