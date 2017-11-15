from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Alliance
from core.reddit import get_subreddit


class Command(BaseCommand):
    help = "Updates reddit flairs and CSS"

    def handle(self, *args, **options):
        sub = get_subreddit()
        alliances = Alliance.objects.filter(active=True).all()
