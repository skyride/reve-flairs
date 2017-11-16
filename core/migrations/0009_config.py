# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alliance_generic_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alliance_sprite', models.CharField(default=None, max_length=32, null=True)),
                ('corp_spite', models.CharField(default=None, max_length=32, null=True)),
                ('style_size', models.IntegerField(default=None, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
