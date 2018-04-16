from django.conf.urls import url
from django.contrib import admin
from django.http import (
    Http404,
    HttpResponseRedirect,
)
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from .models import (
    Inscricao,
    SocioEconomico,
    Recurso,
)

from .forms import ReservaForm

admin.site.register(SocioEconomico)
admin.site.register(Recurso)


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    date_heirarchy = (
        'updated',
    )
    list_display = (
        'id',
        'candidato',
        'curso',
        'local_prova',
        'reserva',
        'socio_economico',
        'acoes_inscricao',
    )
    readonly_fields = (
        'id',
        'candidato',
        'cidade_curso',
        'curso',
        'local_prova',
        'modalidade',
        'reserva',
        'socio_economico',
        'acoes_inscricao',
        'valor',
        'necessidade_esp',
    )
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
            html = 'Não há ações'
        return html
    acoes_inscricao.short_description = 'Ações Inscrição'
    acoes_inscricao.allow_tags = True

    def reserva(self, request, id, *args, **kwargs):
        inscricao = self.get_object(request, id)
        if inscricao.reserva is None:
            raise Http404('Página não encontrada')

        acao_titulo = 'Reserva de Vagas'
        tipo = 'reserva'
        recurso = Recurso.objects.filter(inscricao=inscricao.id, tipo__exact=tipo).first()
        form = ReservaForm(request.POST or None, instance=recurso)

        if request.method == 'POST':
            if form.is_valid():
                status = form.cleaned_data.get('status')
                form_obj = form.save(commit=False)
                if status == '3':  # Indeferido
                    form_obj.inscricao = inscricao
                    form_obj.tipo = tipo
                    form_obj.save()
                    inscricao.reserva = 3  # Indeferido
                    inscricao.save()
                    return redirect('admin:inscricoes_inscricao_changelist')
                elif status == '2':  # Deferido
                    inscricao.reserva = 2  # Indeferido
                    inscricao.save()
                    try:
                        form_obj.save()
                    except:
                        pass
                    return redirect('admin:inscricoes_inscricao_changelist')
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['title'] = acao_titulo
        return TemplateResponse(request, 'admin/account/account_action.html', context)

    def socio(self, request, id, *args, **kwargs):
        inscricao = self.get_object(request, id)
        if inscricao.socio_economico is None:
            raise Http404('Página não encontrada')

        acao_titulo = 'Socioeconômico'
        tipo = 'socio'
        recurso = Recurso.objects.filter(inscricao=inscricao.id, tipo__exact=tipo).first()
        form = ReservaForm(request.POST or None, instance=recurso)

        if request.method == 'POST':
            if form.is_valid():
                status = form.cleaned_data.get('status')
                if status == '3':  # Indeferido
                    form_obj = form.save(commit=False)
                    form_obj.inscricao = inscricao
                    form_obj.tipo = tipo
                    form_obj.save()
                    inscricao.socio_economico = 3  # Indeferido
                    inscricao.valor = '100,00'
                    inscricao.save()
                    return redirect('admin:inscricoes_inscricao_changelist')
                elif status == '2':  # Deferido
                    inscricao.socio_economico = 2  # Deferido
                    inscricao.valor = form.cleaned_data.get('valor')
                    inscricao.save()
                    try:
                        form.save()
                    except:
                        pass
                    return redirect('admin:inscricoes_inscricao_changelist')
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['title'] = acao_titulo
        return TemplateResponse(request, 'admin/account/account_action.html', context)

