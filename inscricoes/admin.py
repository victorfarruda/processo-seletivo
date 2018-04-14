from django.contrib import admin

from .models import Inscricao
from .models import Socioeconomico

admin.site.register(Inscricao)
admin.site.register(Socioeconomico)