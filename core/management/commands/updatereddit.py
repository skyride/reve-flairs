import praw

from django.core.management.base import BaseCommand

from core.models import Alliance


class Command(BaseCommand):
    help = "Updates reddit flairs and CSS"

    def handle(self, *args, **options):
        
