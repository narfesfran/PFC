# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cat_preferidas',
            field=multiselectfield.db.fields.MultiSelectField(max_length=17, null=True, blank=True, verbose_name='Categorías', choices=[(0, 'Arte y Diseño'), (1, 'Arquitectura'), (2, 'Historia'), (3, 'Ciencia y Tecnología'), (4, 'Naturaleza'), (5, 'Aventura'), (6, 'Literatura'), (7, 'Música'), (8, 'Vida urbana')]),
        ),
    ]
