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

from .views import inicio
from inscricoes.views import inscricao
from contas.views import login_page
from cursos.views import get_cursos, get_curso


urlpatterns = [
    url(r'^$', inicio, name='inicio'),
    url(r'^login/$', login_page, name='login'),
    url(r'^inscricao/$', inscricao, name='inscricao'),
    url(r'^inscricao/get_cursos/(?P<id>\d+)$', get_cursos, name='cursos'),
    url(r'^inscricao/get_curso/(?P<id>\d+)$', get_curso, name='curso'),
    url(r'^admin/', admin.site.urls),
]
