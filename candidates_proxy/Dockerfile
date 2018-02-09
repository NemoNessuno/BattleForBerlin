FROM python:3.6-alpine3.7

WORKDIR /app

ADD app.py requirements.txt ./
RUN \
  apk update && \
  apk add build-base && \
  pip install Flask requests gunicorn gevent && \
  apk del build-base

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:8000", "-k", "gevent", "app:app"]
