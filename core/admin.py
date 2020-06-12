# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html

from .models import Alliance, Corp, Generic


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("logo_preview", )

    def logo_preview(self, obj):
        return format_html('<img src="{}" />'.format(obj.logo.url))


@admin.register(Alliance)
class AllianceAdmin(BaseAdmin):
    list_display = (
        "name", "ticker", "alliance_id", "active", "generic_logo", "characters", "active_chars")
    list_filter = ("active", "generic_logo")
    readonly_fields = ("logo_preview", )

    def logo_preview(self, obj):
        return format_html('<img src="{}" />'.format(obj.logo.url))


@admin.register(Corp)
class CorpAdmin(BaseAdmin):
    list_display = ("name", "ticker", "corp_id", "member_count")
    list_filter = ("active", )


@admin.register(Generic)
class GenericAdmin(BaseAdmin):
    list_display = ("name", "active")
    list_filter = ("active", )
