# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-21 12:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20170921_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.City'),
        ),
    ]
