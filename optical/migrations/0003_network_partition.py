# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-11 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('optical', '0002_auto_20181010_2330'),
    ]

    operations = [
        migrations.CreateModel(
            name='network_partition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
            ],
        ),
    ]
