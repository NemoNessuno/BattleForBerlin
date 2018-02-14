FROM python:3.6-alpine3.7

WORKDIR /app

ADD ./requirements.txt ./app.py ./
ADD ./templates/*.html ./templates/

RUN apk update && \
  apk add build-base libffi-dev && \
  pip install -r requirements.txt && \
  apk del build-base

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:8000", "app:app"]
