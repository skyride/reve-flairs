import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.crypto import get_random_string
from csscompressor import compress

from core.models import Alliance, Corp
from core.reddit import get_subreddit
from core.images import generate_spritesheet, calc_location


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

        # Get final lists
        alliances = Alliance.objects.filter(active=True).all()
        corps = Corp.objects.filter(active=True).all()

        # Generate sprite sheets
        alliance_sprite = generate_spritesheet(alliances, "alliances.png")
        corp_sprite = generate_spritesheet(corps, "corps.png")

        # Upload sprite sheets
        alliance_sprite_name = "a-%s" % get_random_string(3)
        corp_sprite_name = "c-%s" % get_random_string(3)
        sub.stylesheet.upload(alliance_sprite_name, alliance_sprite)
        sub.stylesheet.upload(corp_sprite_name, corp_sprite)

        # Generate CSS
        base_css = requests.get(settings.SUBREDDIT_CSS_URL).text
        flair_css = ""

        for i, alliance in enumerate(alliances):
            x, y = calc_location(i)
            css = ".flair-a%i { background: url(%%%%%s%%%%) -%ipx -%ipx no-repeat; text-indent: 30px; min-width: 28px; height: 25px; } " % (
                alliance.id,
                alliance_sprite_name,
                x,
                y
            )
            flair_css = flair_css + css
        css = compress(base_css + flair_css)

        print len(css.encode("utf-8"))
        sub.stylesheet.update(css)
