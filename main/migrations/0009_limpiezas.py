# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-12-13 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_inventario'),
    ]

    operations = [
        migrations.CreateModel(
            name='limpiezas',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('clli', models.CharField(max_length=25)),
                ('fecha', models.CharField(max_length=40)),
                ('observacion', models.CharField(max_length=40)),
            ],
        ),
    ]