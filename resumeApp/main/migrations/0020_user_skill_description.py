# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-22 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20170922_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_skill',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
