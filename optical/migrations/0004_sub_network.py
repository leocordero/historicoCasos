# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-11 19:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('optical', '0003_network_partition'),
    ]

    operations = [
        migrations.CreateModel(
            name='sub_network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('network_partition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optical.network_partition')),
            ],
        ),
    ]
