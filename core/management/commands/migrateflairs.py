import requests
from django.core.management.base import BaseCommand
from django.conf import settings

from core.reddit import get_subreddit
from core.models import Corp, Alliance, Generic


class Command(BaseCommand):
    help = "Migrates user flairs based on the flair name"
    sub = get_subreddit()

    def handle(self, *args, **options):
        # Iterate through all user flairs
        for i, flair in enumerate(self.sub.flair(limit=None)):
            msg = self.handle_user(flair)
            if msg != None:
                print i, msg


    def handle_user(self, flair):
        # Check for alliance
        alliance = Alliance.objects.filter(active=True, name=flair['flair_text'])
        if alliance.exists():
            alliance = alliance.first()
            if alliance.css_class != flair['flair_css_class']:
                self.change_flair(flair['user'], alliance)
                return "Change %s to CSS class %s" % (flair['user'].name, alliance.css_class)
            else:
                return "Redditor %s already has the right CSS class" % flair['user'].name

        # Check for corp
        corp = Corp.objects.filter(name=flair['flair_text'])
        if corp.exists():
            corp = corp.first()
            if corp.css_class != flair['flair_css_class']:
                self.change_flair(flair['user'], corp)
                return "Change %s to CSS class %s" % (flair['user'].name, corp.css_class)
            else:
                return "Redditor %s already has the right CSS class" % flair['user'].name


    def change_flair(self, redditor, new_flair):
        self.sub.flair.update([redditor], text=new_flair.name, css_class=new_flair.css_class)
