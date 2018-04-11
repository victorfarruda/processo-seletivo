from django.db import models

class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    rua         = models.CharField(max_length=120)
    numero      = models.CharField(max_length=10)
    complemento = models.CharField(max_length=120, blank=True, null=True)
    bairro      = models.CharField(max_length=120)
    cidade      = models.CharField(max_length=120)
    estado      = models.CharField(max_length=3)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.rua, self.numero)