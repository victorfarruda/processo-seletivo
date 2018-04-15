from django.conf.urls import url
from django.contrib import admin
from django.http import (
    Http404,
    HttpResponseRedirect,
)
from django.urls import reverse
from django.template.response import TemplateResponse


from . import errors

from .models import Inscricao
from .models import SocioEconomico

from .forms import InscricaoForm

admin.site.register(SocioEconomico)


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'updated',
    )
    list_display = (
        'id',
        'candidato',
        'cidade_curso',
        'curso',
        'local_prova',
        'modalidade',
        'reserva',
        'socio_economico',
        'acoes_inscricao',
    )
    # readonly_fields = (
    #     'id',
    #     'candidato',
    #     'cidade_curso',
    #     'curso',
    #     'local_prova',
    #     'modalidade',
    #     'reserva',
    #     'socio_economico',
    #     'acoes_inscricao',
    # )
    list_select_related = (
        'candidato',
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<id>.+)/reserva/$',
                self.admin_site.admin_view(self.reserva),
                name='reserva',
            ),
            url(
                r'^(?P<id>.+)/socio/$',
                self.admin_site.admin_view(self.socio),
                name='socioeconomico',
            ),
        ]
        return custom_urls + urls

    def acoes_inscricao(self, obj):
        html_reserva = ''
        if obj.reserva is not None:
            html_reserva = '<a class="button" href="{}">Reserva</a>&nbsp;'.format(reverse('admin:reserva', args=[obj.pk]))
        html_socio = ''
        if obj.socio_economico is not None:
            html_socio = '<a class="button" href="{}">Socioeconômico</a>'.format(reverse('admin:socioeconomico', args=[obj.pk]))
        html = html_reserva + html_socio
        if html == '':
            html == 'Não há ações'
        return html
    acoes_inscricao.short_description = 'Ações Inscrição'
    acoes_inscricao.allow_tags = True

    def reserva(self, request, id, *args, **kwargs):
        return self.acao(
            request=request,
            inscricao_id=id,
            form_acao=InscricaoForm,
            acao_titulo='Reserva',
        )

    def socio(self, request, id, *args, **kwargs):
        return self.acao(
            request=request,
            inscricao_id=id,
            form_acao=InscricaoForm,
            acao_titulo='Socioeconômico',
        )

    def acao(
            self,
            request,
            inscricao_id,
            form_acao,
            acao_titulo,
    ):
        inscricao = self.get_object(request, inscricao_id)
        if inscricao.reserva is None and acao_titulo == 'Reserva':
            raise Http404('Página não encontrada')
        if inscricao.socio_economico is None and acao_titulo == 'Socioeconômico':
            raise Http404('Página não encontrada')
        if request.method != 'POST':
            form = form_acao()
        else:
            form = form_acao(request.POST)
            if form.is_valid():
                try:
                    form.save(inscricao, request.user)
                except errors.Error as e:
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'admin:account_account_change',
                        args=[inscricao.pk],
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['inscricao'] = inscricao
        context['title'] = acao_titulo
        return TemplateResponse(
            request,
            'admin/account/account_action.html',
            context,
        )