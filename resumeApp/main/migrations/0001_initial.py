# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-19 14:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=6)),
                ('code', models.CharField(max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Country')),
            ],
        ),
    ]
