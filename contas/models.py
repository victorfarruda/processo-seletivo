from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from enderecos.models import Endereco

# class Perfil(models.Model):
#     nome = models.CharField(max_length=120)
#     sobrenome = models.CharField(max_length=120)
#     data_nasc = models.DateField()
#     telefone = models.CharField(max_length=20)
#     rg        = models.CharField(max_length=20, unique=True)
#     cpf       = models.CharField(max_length=15, unique=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     updated   = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.nome

class Usuario(AbstractBaseUser):
    email = models.CharField(max_length=120, unique=True)
    # perfil = models.OneToOneField(Perfil)
    endereco = models.OneToOneField(Endereco)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.perfil

