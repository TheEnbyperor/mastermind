# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20171231_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]