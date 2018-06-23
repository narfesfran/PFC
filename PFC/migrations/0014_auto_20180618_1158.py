# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0013_remove_photo_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(verbose_name='Longitud', decimal_places=7, validators=[django.core.validators.MaxValueValidator(70.0), django.core.validators.MinValueValidator(-70.0)], max_digits=9),
        ),
    ]
