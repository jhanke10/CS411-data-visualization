# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20170420_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='source',
        ),
        migrations.RemoveField(
            model_name='data',
            name='time',
        ),
        migrations.AddField(
            model_name='data',
            name='create_time',
            field=models.IntegerField(default=1492683104016.502),
        ),
        migrations.AddField(
            model_name='data',
            name='source_id',
            field=models.CharField(default=123, editable=False, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='upload_time',
            field=models.IntegerField(default=1492683104016.4722, editable=False),
        ),
    ]
