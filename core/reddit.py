import praw

from django.conf import settings


def get_reddit():
    return praw.Reddit(client_id=settings.PRAW_CLIENT_ID,
                       client_secret=settings.PRAW_CLIENT_SECRET,
                       username=settings.PRAW_USERNAME,
                       password=settings.PRAW_PASSWORD,
                       user_agent="reve flairbot")

def get_subreddit():
    return get_reddit().subreddit(settings.PRAW_SUBREDDIT)
