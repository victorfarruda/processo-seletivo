from django.db import models

from cursos.models import Curso

class Cidade(models.Model):
    cidade = models.CharField(max_length=120)
    curso  = models.ManyToManyField(Curso)

    def __str__(self):
        return self.cidade