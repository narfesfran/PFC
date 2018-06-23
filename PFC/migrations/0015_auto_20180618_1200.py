# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0014_auto_20180618_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(decimal_places=7, verbose_name='Longitud', max_digits=9, validators=[django.core.validators.MaxValueValidator(180.0), django.core.validators.MinValueValidator(-70.0)]),
        ),
    ]
