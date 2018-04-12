"""processo_uab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from .views import inicio_page
from inscricoes.views import (
    inscricao_page,
    minha_inscricao,
    comprovante_inscricao
)
from contas.views import (
    login_page,
    logout_page,
    meus_dados
)
from cursos.views import (
    get_cursos,
    get_curso
)


urlpatterns = [
    url(r'^$', inicio_page, name='inicio'),
    url(r'^login/$', login_page, name='login'),
    url(r'^logout/$', logout_page, name='logout'),
    url(r'^candidato/dados/$', meus_dados, name='meus_dados'),
    url(r'^candidato/inscricao/$', minha_inscricao, name='minha_inscricao'),
    url(r'^candidato/comprovante/$', comprovante_inscricao, name='comprovante_inscricao'),
    url(r'^inscricao/$', inscricao_page, name='inscricao'),
    url(r'^inscricao/get_cursos/(?P<id>\d+)$', get_cursos, name='cursos'),
    url(r'^inscricao/get_curso/(?P<id>\d+)$', get_curso, name='curso'),
    url(r'^admin/', admin.site.urls),
]
