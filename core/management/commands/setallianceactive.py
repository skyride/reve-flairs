import requests
from django.core.management.base import BaseCommand

from core.models import Alliance


class Command(BaseCommand):
    help = "Sets active states for alliances"

    def handle(self, *args, **options):
        # Get largest alliances
        largest_alliances = list(Alliance.objects.order_by('-characters').values_list('alliance_id', flat=True)[:200])

        # Get the most active pvp alliances
        active_alliances = list(Alliance.objects.order_by('-recent_kills').values_list('alliance_id', flat=True)[:200])

        id_set = set(largest_alliances + active_alliances)
        print len(id_set)

        # Update active
        print "Updating database"
        Alliance.objects.filter(active=True).update(active=False)
        Alliance.objects.filter(alliance_id__in=largest_alliances).update(active=True)

        print "Done!"
