# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0002_auto_20180606_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='css',
            field=models.CharField(max_length=10, blank=True, null=True),
        ),
    ]
