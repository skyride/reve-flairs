from __future__ import unicode_literals

from django.db import models


class Corp(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    ticker = models.CharField(max_length=5)
    logo = models.ImageField(upload_to="corps")


class Alliance(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    ticker = models.CharField(max_length=5)
    logo = models.ImageField(upload_to="alliances")
