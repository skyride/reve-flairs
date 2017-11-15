from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Alliance
from core.reddit import get_subreddit


class Command(BaseCommand):
    help = "Updates reddit flairs and CSS"

    def handle(self, *args, **options):
        sub = get_subreddit()


        # Remove inactive alliance flairs and build the alliance flair list
        live_alliance_flairs = []
        for flair in sub.flair.templates:
            alliance = Alliance.objects.filter(name=flair['flair_text']).first()
            if alliance != None:
                if alliance.active:
                    live_alliance_flairs.append(alliance.id)
                else:
                    # Remove the alliance
                    sub.flair.templates.delete(flair['flair_template_id'])
                    print "Removed %s as it was no longer active" % alliance.name

        # Add newly active alliance flairs
        for alliance in Alliance.objects.filter(active=True).exclude(id__in=live_alliance_flairs).all():
            sub.flair.templates.add(alliance.name, css_class="a%i" % alliance.id, text_editable=False)
            print "Added %s" % alliance.name
