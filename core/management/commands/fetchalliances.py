import requests

from django.core.management.base import BaseCommand

from core.models import Alliance


class Command(BaseCommand):
    help = "Fetches all alliances in EVE Online"

    def handle(self, *args, **options):
        print "Fetching alliance list..."
        alliance_ids = requests.get("https://esi.tech.ccp.is/latest/alliances/").json()
        print "%i alliances in the list, starting..." % len(alliance_ids)

        for i, id in enumerate(alliance_ids):
            alliance = Alliance.fetch(id)

            if alliance.closed:
                print "(%s/%s) Fetched %s, closed" % (i+1, len(alliance_ids), alliance.name)
            else:
                print "(%s/%s) Fetched %s, open with %s corps" % (i+1, len(alliance_ids), alliance.name, alliance.corp_count)

        print "Done!"
