# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 12:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_degree'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='degree',
            name='year',
        ),
    ]
