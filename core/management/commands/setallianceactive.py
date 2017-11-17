import requests
from django.core.management.base import BaseCommand

from core.models import Alliance


class Command(BaseCommand):
    help = "Sets active states for alliances"

    def handle(self, *args, **options):
        # Get largest alliances
        largest_alliances = list(Alliance.objects.filter(generic_logo=False).order_by('-characters').values_list('alliance_id', flat=True)[:150])

        # Get the most active pvp alliances
        active_alliances = list(Alliance.objects.filter(generic_logo=False).order_by('-recent_kills').values_list('alliance_id', flat=True)[:250])

        # Get special alliances
        special_alliances = list(Alliance.objects.filter(
            generic_logo=False,
            name__in=[
                "Black Legion.",
                "Circle-Of-Two",
                "SpaceMonkey's Alliance"
            ]
        ).values_list('alliance_id', flat=True))

        krabs = set(largest_alliances) - set(active_alliances)
        #print Alliance.objects.filter(alliance_id__in=krabs).all()
        id_set = set(largest_alliances + active_alliances + special_alliances)
        print len(id_set)

        # Update active
        print "Updating database"
        Alliance.objects.filter(active=True).update(active=False)
        Alliance.objects.filter(alliance_id__in=id_set).update(active=True)

        print "Done!"
