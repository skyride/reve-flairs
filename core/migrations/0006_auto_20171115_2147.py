# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 21:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20171115_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alliance',
            name='active',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='alliance',
            name='alliance_id',
            field=models.BigIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='corp',
            name='corp_id',
            field=models.BigIntegerField(db_index=True),
        ),
    ]
