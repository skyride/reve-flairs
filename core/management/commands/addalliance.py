import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Alliance


class Command(BaseCommand):
    help = "Add alliance"

    def add_arguments(self, parser):
        parser.add_argument('alliance_id', nargs='+', type=int)

    def handle(self, *args, **options):
        alliance = Alliance.fetch(options['alliance_id'][0])
        print alliance
