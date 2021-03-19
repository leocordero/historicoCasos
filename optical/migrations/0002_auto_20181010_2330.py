# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-10-10 23:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('optical', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='area_divisional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='dir_divisional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='area_divisional',
            name='dir_divisional',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='optical.dir_divisional'),
        ),
    ]