# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0008_auto_20180609_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='css',
            field=models.CharField(verbose_name='Estilo de la web', choices=[('1', 'CLARO'), ('2', 'OSCURO')], default='1', max_length=1),
        ),
    ]
