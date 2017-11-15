from __future__ import unicode_literals

import os
import requests
import urllib

from django.db import models
from django.conf import settings
from django.core.files import File


class Corp(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    ticker = models.CharField(max_length=5)
    logo = models.ImageField(upload_to="corps")
    active = models.BooleanField(default=False)

    @staticmethod
    def fetch(id):
        # Get data
        corp = requests.get("https://esi.tech.ccp.is/latest/corporations/%s/" % id)
        if corp.status_code != 200:
            return None

        # Get image
        logo = urllib.urlretrieve("https://imageserver.eveonline.com/Corporation/%s_128.png" % id)

        # Build corp object
        corp = corp.json()
        db_corp = Corp(
            id=id,
            name=corp['corporation_name'],
            ticker=corp['ticker']
        )
        db_corp.save()
        db_corp.logo.save(
            "corp_%s.png" % id,
            File(open(logo[0]))
        )

        return db_corp

    def __str__(self):
        return "%s:%s" % (self.id, self.name)



class Alliance(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    ticker = models.CharField(max_length=5)
    logo = models.ImageField(upload_to="alliances")
    active = models.BooleanField(default=False)

    @staticmethod
    def fetch(id):
        # Get data
        alliance = requests.get("https://esi.tech.ccp.is/latest/alliances/%s/" % id)
        if alliance.status_code != 200:
            return None

        # Get image
        logo = urllib.urlretrieve("https://imageserver.eveonline.com/Alliance/%s_128.png" % id)

        # Build alliance object
        alliance = alliance.json()
        db_alliance = Alliance(
            id=id,
            name=alliance['alliance_name'],
            ticker=alliance['ticker']
        )
        db_alliance.save()
        db_alliance.logo.save(
            "alliance_%s.png" % id,
            File(open(logo[0]))
        )

        return db_alliance

    def __str__(self):
        return "%s:%s" % (self.id, self.name)
