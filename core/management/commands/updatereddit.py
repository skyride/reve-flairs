from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Alliance, Corp
from core.reddit import get_subreddit
from core.images import generate_spritesheet


class Command(BaseCommand):
    help = "Updates reddit flairs and CSS"

    def handle(self, *args, **options):
        sub = get_subreddit()


        # Remove inactive alliance flairs and build the alliance flair list
        live_flairs = []
        for flair in sub.flair.templates:
            alliance = Alliance.objects.filter(name=flair['flair_text']).first()
            if alliance != None:
                if alliance.active:
                    live_flairs.append(alliance.id)
                else:
                    # Remove the alliance
                    sub.flair.templates.delete(flair['flair_template_id'])
                    print "Removed %s" % alliance.name

        # Add newly active alliance flairs
        for alliance in Alliance.objects.filter(active=True).exclude(id__in=live_flairs).all():
            sub.flair.templates.add(alliance.name, css_class="a%i" % alliance.id, text_editable=False)
            print "Added %s" % alliance.name

        # Remove inactive corp flairs and build the corp flair list
        live_flairs = []
        for flair in sub.flair.templates:
            corp = Corp.objects.filter(name=flair['flair_text']).first()
            if corp != None:
                if corp.active:
                    live_flairs.append(corp.id)
                else:
                    # Remove the corp
                    sub.flair.templates.delete(flair['flair_template_id'])
                    print "Removed %s" % corp.name

        # Add newly active corp flairs
        for corp in Corp.objects.filter(active=True).exclude(id__in=live_flairs).all():
            sub.flair.templates.add(corp.name, css_class="c%i" % corp.id, text_editable=False)
            print "Added %s" % corp.name

        print generate_spritesheet(Alliance.objects.filter(active=True).all(), "alliances.png")
        print generate_spritesheet(Corp.objects.filter(active=True).all(), "corps.png")
