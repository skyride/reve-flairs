import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from core.models import Alliance, Corp, Generic, Redditor, RedditorFlair
from core.reddit import get_subreddit


class Command(BaseCommand):
    help = "Collect flair stats from reddit API"
    sub = get_subreddit()

    def handle(self, *args, **options):
        for i, flair in enumerate(self.sub.flair(limit=None)):
            msg = self.handle_flair(flair['user'], flair['flair_css_class'])
            if msg != None:
                print i, flair['user'].name, msg


    def handle_flair(self, redditor, css_class):
        # Get redditor db object
        try:
            db_redditor = Redditor.objects.get(name=redditor.name)
        except Redditor.DoesNotExist:
            db_redditor = Redditor(name=redditor.name)
            db_redditor.save()

        # End the current redditorflair
        if db_redditor.flair != None:
            old_flair = db_redditor.flair
            if old_flair.css_class != css_class:
                old_flair.ended = timezone.now()
                old_flair.save()

                return self.create_flair(db_redditor, css_class)
        else:
            return self.create_flair(db_redditor, css_class)


    def create_flair(self, db_redditor, css_class):
        rf = RedditorFlair(redditor=db_redditor)

        if css_class != None:
            try:
                css_id = int(css_class[1:])
                if css_class[0] == "g":
                    g = Generic.objects.filter(id=css_id)
                    if g.exists():
                        rf.generic = g.first()
                        rf.save()
                        return "Flair set to Generic %s:%s" % (rf.generic.id, rf.generic.name)

                if css_class[0] == "a":
                    a = Alliance.objects.filter(id=css_id)
                    if a.exists():
                        rf.alliance = a.first()
                        rf.save()
                        return "Flair set to Alliance %s:%s" % (rf.alliance.id, rf.alliance.name)

                if css_class[0] == "c":
                    c = Corp.objects.filter(id=css_id)
                    if c.exists():
                        rf.corp = c.first()
                        rf.save()
                        return "Flair set to Corp %s:%s" % (rf.corp.id, rf.corp.name)
            except ValueError:
                pass
