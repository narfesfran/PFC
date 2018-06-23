# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0003_profile_css'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='css',
            field=multiselectfield.db.fields.MultiSelectField(null=True, blank=True, max_length=15, verbose_name='Tema de fondo', choices=[('original', 'Claro'), ('oscuro', 'Oscuro')]),
        ),
    ]
