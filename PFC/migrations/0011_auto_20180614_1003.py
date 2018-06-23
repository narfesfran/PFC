# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PFC', '0010_auto_20180614_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('thumbnail', models.ImageField(upload_to='', verbose_name='Miniatura')),
                ('place', models.ForeignKey(to='PFC.Place', verbose_name='Lugar de referencia')),
            ],
        ),
        migrations.RemoveField(
            model_name='photo',
            name='thumbnail',
        ),
    ]
