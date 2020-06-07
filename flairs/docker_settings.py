import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = bool(int(os.environ.get("DEBUG", "0")))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['DB_HOST'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'PORT': os.environ.get('DB_PORT', '')
    }
}

PRAW_CLIENT_ID = os.environ['PRAW_CLIENT_ID']
PRAW_CLIENT_SECRET = os.environ['PRAW_CLIENT_SECRET']
PRAW_USERNAME = os.environ['PRAW_USERNAME']
PRAW_PASSWORD = os.environ['PRAW_PASSWORD']
PRAW_SUBREDDIT = os.environ.get('PRAW_SUBREDDIT', "eve")

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("SENTRY_ENVIRONMENT"),
    release=os.environ['TAG'],
    integrations=[DjangoIntegration()],
    send_default_pii=True)
