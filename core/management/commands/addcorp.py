import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Corp


class Command(BaseCommand):
    help = "Add a corp"

    def add_arguments(self, parser):
        parser.add_argument('corp_id', nargs='+', type=int)

    def handle(self, *args, **options):
        corp = Corp.fetch(options['corp_id'][0], active=True)
        print corp
