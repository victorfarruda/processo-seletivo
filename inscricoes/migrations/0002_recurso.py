# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-15 19:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inscricoes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(2, 'Deferido'), (3, 'Indeferido')], max_length=120)),
                ('motivo_indeferimento', models.TextField()),
                ('recurso', models.TextField(blank=True, null=True)),
                ('resposta_recurso', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('reserva', 'Reserva de Vagas'), ('socio', 'Socioeconômico')], max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('inscricao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscricoes.Inscricao')),
            ],
        ),
    ]
