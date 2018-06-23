# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0006_remove_profile_css'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='css',
            field=multiselectfield.db.fields.MultiSelectField(null=True, verbose_name='Tema de fondo', choices=[('claro', 'Tema claro'), ('oscuro', 'Tema oscuro')], max_length=12, blank=True),
        ),
    ]
