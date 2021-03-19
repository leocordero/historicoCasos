# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-12 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('optical', '0009_auto_20181012_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipo_optical',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='optical.cliente'),
        ),
        migrations.AlterField(
            model_name='equipo_optical',
            name='central',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.central'),
        ),
    ]
