# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-12 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optical', '0008_auto_20181012_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo_optical',
            name='status',
            field=models.CharField(default='Active', max_length=10, null=True),
        ),
    ]
