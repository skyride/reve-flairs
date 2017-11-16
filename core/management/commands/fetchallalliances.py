import requests

from django.core.management.base import BaseCommand

from core.models import Alliance


class Command(BaseCommand):
    help = "Fetches all alliances in EVE Online"

    def handle(self, *args, **options):
        print "Fetching full alliance list..."
        alliance_ids = requests.get("https://esi.tech.ccp.is/latest/alliances/").json()
        alliance_ids = alliance_ids
        print "%i alliances in the list, starting..." % len(alliance_ids)

        for i, id in enumerate(alliance_ids):
            # Get data from esi
            alliance = Alliance.fetch(id)

            # Get data from zkill
            zkill = requests.get("https://zkillboard.com/api/stats/allianceID/%s/" % id).json()
            if zkill != None:
                try:
                    alliance.characters = zkill['info']['memberCount']
                except KeyError:
                    print "Failed to fetch meta data from zkill"

                try:
                    alliance.ships_destroyed = zkill['shipsDestroyed']
                except KeyError:
                    print "Failed to fetch ships destroyed from zkill"

                try:
                    alliance.active_chars = zkill['activepvp']['characters']['count']
                    alliance.recent_kills = zkill['activepvp']['kills']['count']
                except KeyError:
                    print "Failed to fetch active pvp data from zkill"
                alliance.save()

            else:
                print "Failed to get any from zkill"

            if alliance.closed:
                print "(%s/%s) Fetched %s, closed" % (i+1, len(alliance_ids), alliance.name)
            else:
                print "(%s/%s) Fetched %s, open with %s members and %s corps" % (i+1, len(alliance_ids), alliance.name, alliance.characters, alliance.corp_count)

        print "Done!"
