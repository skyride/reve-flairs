import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.crypto import get_random_string
from csscompressor import compress

from core.models import Alliance, Corp, Config
from core.reddit import get_subreddit
from core.images import generate_spritesheet, calc_location


class Command(BaseCommand):
    help = "Updates reddit flairs and CSS"

    def handle(self, *args, **options):
        sub = get_subreddit()


        # Remove inactive alliance flairs and build the alliance flair list
        print "Removing inactive alliance flairs"
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
        print "Adding newly active alliance flairs"
        for alliance in Alliance.objects.filter(active=True).exclude(id__in=live_flairs).all():
            sub.flair.templates.add(alliance.name, css_class=alliance.css_class, text_editable=False)
            print "Added %s" % alliance.name

        # Remove inactive corp flairs and build the corp flair list
        print "Removing inactive corp flairs"
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
        print "Adding newly active corp flairs"
        for corp in Corp.objects.filter(active=True).exclude(id__in=live_flairs).all():
            sub.flair.templates.add(corp.name, css_class="c%i" % corp.id, text_editable=False)
            print "Added %s" % corp.name

        # Get final lists
        alliances = Alliance.objects.filter(active=True).all()
        corps = Corp.objects.filter(active=True).all()
        print "Getting final list of active alliances (%s) and corps (%s)" % (
            alliances.count(),
            corps.count()
        )

        # Generate sprite sheets
        print "Generating alliance spritesheet"
        alliance_sprite = generate_spritesheet(alliances, "alliances.png")
        print "Generating corp spritesheet"
        corp_sprite = generate_spritesheet(corps, "corps.png")

        # Delete old spritesheets
        print "Deleting old spritesheets"
        config = Config.get_solo()
        if config.alliance_sprite != None:
            sub.stylesheet.delete_image(config.alliance_sprite)
            sub.stylesheet.delete_image(config.corp_sprite)

        # Upload sprite sheets
        print "Uploading spritesheets"
        alliance_sprite_name = "a"
        corp_sprite_name = "c"
        sub.stylesheet.upload(alliance_sprite_name, alliance_sprite)
        sub.stylesheet.upload(corp_sprite_name, corp_sprite)

        config.alliance_sprite = alliance_sprite_name
        config.corp_sprite = corp_sprite_name

        # Generate CSS
        print "Fetching base CSS from github"
        base_css = requests.get(settings.SUBREDDIT_CSS_URL).text
        flair_css = ""

        print "Generating flair CSS"
        for i, alliance in enumerate(alliances):
            x, y = calc_location(i)
            css = ".flair-%s { background: url(%%%%%s%%%%) %i -%ipx repeat-y } " % (
                alliance.css_class,
                alliance_sprite_name,
                x,
                y
            )
            flair_css = flair_css + css

        for i, corp in enumerate(corps):
            x, y = calc_location(i)
            css = ".flair-%s { background: url(%%%%%s%%%%) %i -%ipx repeat-y } " % (
                corp.css_class,
                corp_sprite_name,
                x,
                y
            )
            flair_css = flair_css + css

        print "Compressing..."
        css = compress(base_css + flair_css)
        config.style_size = len(css.encode("utf-8"))
        config.save()
        print config.style_size, "bytes"

        print "Uploading CSS Sheet"
        sub.stylesheet.update(css)
        print "Done!"
