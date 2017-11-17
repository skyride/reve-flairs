from __future__ import unicode_literals

import os
import requests
import urllib
from solo.models import SingletonModel

from django.db import models
from django.conf import settings
from django.core.files import File

from core.images import is_generic_alliance_logo


class Config(SingletonModel):
    alliance_sprite = models.CharField(max_length=32, null=True, default=None)
    corp_sprite = models.CharField(max_length=32, null=True, default=None)
    style_size = models.IntegerField(null=True, default=None)


class Generic(models.Model):
    name = models.CharField(max_length=32, null=True, default=None)
    active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to="generics")

    @property
    def css_class(self):
        return "g%s" % self.id


class Corp(models.Model):
    corp_id = models.BigIntegerField(db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    ticker = models.CharField(max_length=5)
    logo = models.ImageField(upload_to="corps")
    active = models.BooleanField(default=False, db_index=True)
    member_count = models.IntegerField(null=True, default=None)

    @property
    def closed(self):
        return self.member_count < 1

    @property
    def css_class(self):
        return "c%s" % self.id

    @staticmethod
    def fetch(id, active=False):
        # Get data
        corp = requests.get("https://esi.tech.ccp.is/latest/corporations/%s/" % id)
        if corp.status_code != 200:
            return None

        # Get image
        logo = urllib.urlretrieve("https://imageserver.eveonline.com/Corporation/%s_128.png" % id)

        # Build corp object
        corp = corp.json()
        db_corp = Corp.objects.filter(corp_id=id).first()
        if db_corp == None:
            db_corp = Corp(corp_id=id)

        db_corp.name = corp['corporation_name']
        db_corp.ticker = corp['ticker']
        db_corp.member_count = corp['member_count']
        db_corp.active = active

        db_corp.save()
        db_corp.logo.save(
            "corp_%s.png" % id,
            File(open(logo[0]))
        )

        return db_corp

    def __str__(self):
        return "%s:%s" % (self.id, self.name)



class Alliance(models.Model):
    alliance_id = models.BigIntegerField(db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    ticker = models.CharField(max_length=5)
    logo = models.ImageField(upload_to="alliances")
    active = models.BooleanField(default=False, db_index=True)
    corp_count = models.IntegerField(null=True, default=None)
    generic_logo = models.BooleanField(default=True)

    # Zkill data
    characters = models.IntegerField(default=0, db_index=True)
    ships_destroyed = models.IntegerField(default=0, db_index=True)
    active_chars = models.IntegerField(default=0, db_index=True)
    recent_kills = models.IntegerField(default=0, db_index=True)


    @property
    def closed(self):
        return self.corp_count < 1

    @property
    def css_class(self):
        if self.generic_logo:
            return "ag"
        else:
            return "a%s" % self.id

    @staticmethod
    def fetch(id):
        # Get data
        alliance = requests.get("https://esi.tech.ccp.is/latest/alliances/%s/" % id)
        corps = requests.get("https://esi.tech.ccp.is/latest/alliances/%s/corporations/" % id)
        if alliance.status_code != 200:
            return None

        # Get image
        logo = urllib.urlretrieve("https://imageserver.eveonline.com/Alliance/%s_128.png" % id)

        # Build alliance object
        alliance = alliance.json()
        corps = corps.json()
        db_alliance = Alliance.objects.filter(alliance_id=id).first()
        if db_alliance == None:
            db_alliance = Alliance(alliance_id=id)

        db_alliance.name = alliance['alliance_name']
        db_alliance.ticker = alliance['ticker']
        db_alliance.corp_count = len(corps)

        db_alliance.save()
        db_alliance.logo.save(
            "alliance_%s.png" % id,
            File(open(logo[0]))
        )

        # Check if logo is generic
        db_alliance.generic_logo = is_generic_alliance_logo(db_alliance.logo)
        db_alliance.save()

        return db_alliance

    def __str__(self):
        return "%s:%s" % (self.id, self.name)
