# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_time',
            field=models.DateTimeField(blank=True),
        ),
    ]
