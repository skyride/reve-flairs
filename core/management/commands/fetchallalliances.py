import time

import requests
from django.core.management.base import BaseCommand

from core.models import Alliance


class Command(BaseCommand):
    help = "Fetches all alliances in EVE Online"

    def handle(self, *args, **options):
        print "Fetching full alliance list..."
        alliance_ids = requests.get("https://esi.evetech.net/latest/alliances/").json()
        alliance_ids = alliance_ids
        print "%i alliances in the list, starting..." % len(alliance_ids)

        for i, id in enumerate(alliance_ids):
            # Get data from esi
            alliance = Alliance.fetch(id)

            # Get data from zkill
            # If we hit a 429 then wait half a second and retry
            while True:
                time.sleep(0.2)
                response = requests.get("https://zkillboard.com/api/stats/allianceID/%s/" % id)
                if response.status_code == 200:
                    zkill = response.json()
                    break
                elif response.status_code == 429:
                    time.sleep(0.5)

            try:
                try:
                    alliance.characters = zkill['info']['memberCount']
                except KeyError:
                    print "Failed to fetch meta data from zkill"

                alliance.ships_destroyed = zkill.get('shipsDestroyed', 0)

                try:
                    alliance.active_chars = zkill['activepvp']['characters']['count']
                    alliance.recent_kills = zkill['activepvp']['kills']['count']
                except KeyError:
                    alliance.active_chars = 0
                    alliance.recent_kills = 0

                alliance.save()

            except Exception:
                print "Failed to get any from zkill"

            if alliance.closed:
                print "(%s/%s) Fetched %s, closed" % (i+1, len(alliance_ids), alliance.name)
            else:
                print "(%s/%s) Fetched %s, open with %s members and %s corps" % (i+1, len(alliance_ids), alliance.name, alliance.characters, alliance.corp_count)

        print "Done!"
