# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 04:57
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20170420_0449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='data_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='data',
            name='time',
            field=models.IntegerField(default=1492664270033.4438, editable=False),
        ),
        migrations.AlterField(
            model_name='source',
            name='source_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
