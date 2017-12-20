# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Case, When, Sum, Q
from django.utils import timezone
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill

from core.models import *


# Annotation filter to find redditorflair objects with
redditorflair_filter = Sum(
    Case(
        When(redditorflairs__ended__isnull=True, then=1),
        default=0,
        output_field=models.IntegerField()
    )
)
redditorflair_lastweek = Sum(
    Case(
        When(
            Q(
                Q(redditorflairs__ended__isnull=True) | Q(redditorflairs__ended__lt=timezone.now()-timedelta(days=7)),
                redditorflairs__started__lt=timezone.now() - timedelta(days=5),
            ),
            then=1
        ),
        default=0,
        output_field=models.IntegerField()
    )
)


class Thumbnail(ImageSpec):
    processors = [ResizeToFill(38, 38)]
    format = 'PNG'
    options = {'quality': 90}
register.generator('core:logo', Thumbnail)


def all_top100_stats(request):
    alliances = Alliance.objects.filter(
        active=True
    ).annotate(
        flair_count=redditorflair_filter,
        flair_lastweek=redditorflair_lastweek
    ).order_by(
        '-flair_count',
        'name'
    )
    corps = Corp.objects.filter(
        active=True
    ).annotate(
        flair_count=redditorflair_filter,
        flair_lastweek=redditorflair_lastweek
    ).order_by(
        '-flair_count',
        'name'
    )
    generics = Generic.objects.filter(
        active=True
    ).annotate(
        flair_count=redditorflair_filter,
        flair_lastweek=redditorflair_lastweek
    ).order_by(
        '-flair_count',
        'name'
    )

    top = list(alliances) + list(corps) + list(generics)
    top = sorted(top, key=lambda x: x.flair_count, reverse=True)

    context = {
        "header": "Top 100",
        "flairs": enumerate(top[:100])
    }

    return render(request, "core/flair_list.html", context)


def alliance_stats(request):
    alliances = Alliance.objects.filter(
        active=True
    ).annotate(
        flair_count=redditorflair_filter,
        flair_lastweek=redditorflair_lastweek
    ).order_by(
        '-flair_count',
        'name'
    )

    context = {
        "header": "Alliances",
        "flairs": enumerate(alliances)
    }

    return render(request, "core/flair_list.html", context)


def corp_stats(request):
    corps = Corp.objects.filter(
        active=True
    ).annotate(
        flair_count=redditorflair_filter,
        flair_lastweek=redditorflair_lastweek
    ).order_by(
        '-flair_count',
        'name'
    )

    context = {
        "header": "Corps",
        "flairs": enumerate(corps)
    }

    return render(request, "core/flair_list.html", context)


def generic_stats(request):
    generics = Generic.objects.filter(
        active=True
    ).annotate(
        flair_count=redditorflair_filter,
        flair_lastweek=redditorflair_lastweek
    ).order_by(
        '-flair_count',
        'name'
    )

    context = {
        "header": "Generics",
        "flairs": enumerate(generics)
    }

    return render(request, "core/flair_list.html", context)
