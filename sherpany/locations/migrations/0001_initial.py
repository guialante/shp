# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-11-06 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.CharField(max_length=10)),
                ('lng', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
    ]