# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-11 21:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_inventario'),
        ('optical', '0005_equipo_optical'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo_optical',
            name='modelo_equipo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.modelo_equipo'),
        ),
        migrations.AddField(
            model_name='equipo_optical',
            name='network_id',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='equipo_optical',
            name='software_version',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='equipo_optical',
            name='status',
            field=models.CharField(default='Active', max_length=10),
        ),
        migrations.AlterField(
            model_name='equipo_optical',
            name='ne_id',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
