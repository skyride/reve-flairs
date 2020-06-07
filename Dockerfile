FROM python:2.7

WORKDIR /app

RUN apt-get update && \
    apt-get install gcc
RUN pip install --no-cache-dir uWSGI==2.0.18

COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy files
COPY . .
COPY flairs/docker_settings.py flairs/local_settings.py

# Versioning (for Sentry)
ARG TAG=dev
ENV TAG=${TAG}

# Collectstatic
ARG DB_HOST=
ARG DB_NAME=
ARG DB_USER=
ARG DB_PASSWORD=
ARG PRAW_CLIENT_ID=
ARG PRAW_CLIENT_SECRET=
ARG PRAW_USERNAME=
ARG PRAW_PASSWORD=
RUN ./manage.py collectstatic

# Ops Parameters
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WORKERS=1

CMD uwsgi --http :${PORT} --processes ${WORKERS} --static-map /static=/static --static-map /media=/media --module flairs.wsgi:application
