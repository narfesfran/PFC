# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0004_auto_20180609_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='css',
            field=multiselectfield.db.fields.MultiSelectField(null=True, verbose_name='Tema de fondo', max_length=12, blank=True, choices=[('claro', 'claro'), ('oscuro', 'oscuro')]),
        ),
    ]
