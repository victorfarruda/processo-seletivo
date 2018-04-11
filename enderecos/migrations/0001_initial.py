# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-11 20:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cep', models.CharField(max_length=9)),
                ('rua', models.CharField(max_length=120)),
                ('numero', models.CharField(max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=120, null=True)),
                ('bairro', models.CharField(max_length=120)),
                ('cidade', models.CharField(max_length=120)),
                ('estado', models.CharField(max_length=3)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]