# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 14:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20171115_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='alliance',
            name='generic_logo',
            field=models.BooleanField(default=True),
        ),
    ]
