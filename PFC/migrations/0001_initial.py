# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import multiselectfield.db.fields
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('image', models.ImageField(verbose_name='Imagen', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tipo', models.CharField(choices=[('site', 'Sitio'), ('poi', 'Punto de Interés')], max_length=4)),
                ('name', models.CharField(verbose_name='Nombre', max_length=50)),
                ('description', models.TextField(verbose_name='Descripción')),
                ('image', models.ImageField(verbose_name='Imagen de portada', upload_to='')),
                ('latitude', models.DecimalField(verbose_name='Latitud', validators=[django.core.validators.MaxValueValidator(90.0), django.core.validators.MinValueValidator(-90.0)], decimal_places=7, max_digits=9)),
                ('longitude', models.DecimalField(verbose_name='Longitud', validators=[django.core.validators.MaxValueValidator(180.0), django.core.validators.MinValueValidator(-180.0)], decimal_places=7, max_digits=9)),
                ('categorias', multiselectfield.db.fields.MultiSelectField(verbose_name='Categorías', choices=[(0, 'Arte y Diseño'), (1, 'Arquitectura'), (2, 'Historia'), (3, 'Ciencia y Tecnología'), (4, 'Naturaleza'), (5, 'Aventura'), (6, 'Literatura'), (7, 'Música'), (8, 'Vida urbana')], max_length=17)),
                ('url', models.URLField(verbose_name='URL')),
                ('rating', models.IntegerField(verbose_name='Puntuación media', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('votes', models.IntegerField(verbose_name='Número de votos')),
                ('likes', models.IntegerField(blank=True, verbose_name='Número de veces favorito', null=True)),
                ('author', models.IntegerField(blank=True, null=True)),
                ('ref', models.ForeignKey(to='PFC.Place', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tipo', models.CharField(verbose_name='Rol', choices=[('administradores', 'Administrador'), ('usuarios', 'Usuario')], max_length=20)),
                ('nombre', models.CharField(blank=True, verbose_name='Nombre', null=True, max_length=25)),
                ('apellidos', models.CharField(blank=True, verbose_name='Apellidos', null=True, max_length=35)),
                ('correo', models.EmailField(blank=True, verbose_name='Correo electrónico', null=True, max_length=254)),
                ('cat_preferidas', multiselectfield.db.fields.MultiSelectField(verbose_name='Categorías', choices=[(0, 'Arte y Diseño'), (1, 'Arquitectura'), (2, 'Historia'), (3, 'Ciencia y Tecnología'), (4, 'Naturaleza'), (5, 'Aventura'), (6, 'Literatura'), (7, 'Música'), (8, 'Vida urbana')], max_length=17)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Votos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('valor', models.IntegerField(verbose_name='Puntuación media inicial', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('lugar', models.ForeignKey(to='PFC.Place', null=True, blank=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='place',
            field=models.ForeignKey(verbose_name='Lugar de referencia', to='PFC.Place'),
        ),
        migrations.AddField(
            model_name='favoritos',
            name='lugar',
            field=models.ForeignKey(to='PFC.Place', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='favoritos',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]
