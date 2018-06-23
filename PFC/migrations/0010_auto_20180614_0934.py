# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0009_auto_20180612_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumbnail',
            field=models.ImageField(default=1, upload_to='', verbose_name='Miniatura'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='css',
            field=models.CharField(default='1', choices=[('1', 'CLARO'), ('2', 'OSCURO'), ('3', 'SIMPLE')], max_length=1, verbose_name='Estilo de la web'),
        ),
    ]
