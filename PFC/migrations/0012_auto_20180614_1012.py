# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0011_auto_20180614_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thumbnail',
            name='place',
        ),
        migrations.AddField(
            model_name='photo',
            name='thumbnail',
            field=models.CharField(max_length=200, default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Thumbnail',
        ),
    ]
