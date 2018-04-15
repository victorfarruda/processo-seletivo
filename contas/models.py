from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save

from enderecos.models import Endereco

class Perfil(models.Model):
    nome = models.CharField(max_length=120)
    sobrenome = models.CharField(max_length=120)
    data_nasc = models.DateField()
    telefone = models.CharField(max_length=20)
    rg        = models.CharField(max_length=20, unique=True)
    cpf       = models.CharField(max_length=15, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


def post_save_nome_receiver(sender, created, instance, *args, **kwargs):
    if not created:
        usuario = instance.usuario
        usuario.nome = instance.nome
        usuario.save()


post_save.connect(post_save_nome_receiver, sender=Perfil)


class ManagerUsuario(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Usuário deve ter endereço de e-mail')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    nome      = models.CharField(max_length=120, blank=True, null=True)
    email     = models.CharField(max_length=120, unique=True)
    perfil    = models.OneToOneField(Perfil, blank=True, null=True)
    endereco  = models.OneToOneField(Endereco, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin  = models.BooleanField(default=False)
    is_staff  = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = ManagerUsuario()

    # def __str__(self):
    #     return self.nome

    def get_short_name(self):
        return self.nome

    def get_full_name(self):
        return self.perfil.nome + ' ' + self.perfil.sobrenome

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
