# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_auto_20170426_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='create_time',
            field=models.IntegerField(default=1493200803068.65),
        ),
        migrations.AlterField(
            model_name='data',
            name='upload_time',
            field=models.IntegerField(default=1493200803068.623, editable=False),
        ),
    ]