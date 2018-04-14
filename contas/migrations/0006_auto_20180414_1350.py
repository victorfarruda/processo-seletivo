# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-14 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0005_usuario_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
