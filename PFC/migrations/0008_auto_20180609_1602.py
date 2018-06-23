# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0007_profile_css'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='css',
            field=models.CharField(max_length=1, choices=[('1', 'CLARO'), ('2', 'OSCURO')], default='1', verbose_name='Tema de fondo'),
        ),
    ]
