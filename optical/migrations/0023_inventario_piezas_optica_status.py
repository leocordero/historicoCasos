# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-05-28 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optical', '0022_version_inventario'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario_piezas_optica',
            name='status',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]