# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Alliance, Corp, Generic


@admin.register(Alliance)
class AllianceAdmin(admin.ModelAdmin):
    list_display = (
        "name", "ticker", "alliance_id", "active", "generic_logo", "characters", "active_chars")
    list_filter = ("active", "generic_logo")

@admin.register(Corp)
class CorpAdmin(admin.ModelAdmin):
    list_display = ("name", "ticker", "corp_id", "member_count")
    list_filter = ("active", )

@admin.register(Generic)
class GenericAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("active", )
