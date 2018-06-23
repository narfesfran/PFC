# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0015_auto_20180618_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(verbose_name='Longitud', max_digits=10, validators=[django.core.validators.MaxValueValidator(180.0), django.core.validators.MinValueValidator(-180.0)], decimal_places=7),
        ),
    ]
