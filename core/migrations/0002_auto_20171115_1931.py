# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alliance',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='corp',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
