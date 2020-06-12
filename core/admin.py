# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html

from .forms import CorpAddForm
from .models import Alliance, Corp, Generic


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("logo_preview", )

    def logo_preview(self, obj):
        return format_html('<img src="{}" />'.format(obj.logo.url))

    def get_form(self, request, obj=None, **kwargs):
        if not hasattr(self, "_form"):
            self._form = self.form

        if not obj and hasattr(self, "add_form"):
            self.form = self.add_form
        else:
            self.form = self._form

        return super(BaseAdmin, self).get_form(request, obj, **kwargs)


@admin.register(Alliance)
class AllianceAdmin(BaseAdmin):
    list_display = (
        "name", "ticker", "alliance_id", "active", "generic_logo", "characters", "active_chars")
    list_filter = ("active", "generic_logo")
    
    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        return form.save(commit=False)


@admin.register(Corp)
class CorpAdmin(BaseAdmin):
    list_display = ("name", "ticker", "corp_id", "member_count", "active")
    list_filter = ("active", )
    add_form = CorpAddForm


@admin.register(Generic)
class GenericAdmin(BaseAdmin):
    list_display = ("name", "active")
    list_filter = ("active", )
