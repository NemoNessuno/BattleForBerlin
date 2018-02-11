FROM python:2.7-alpine3.7

MAINTAINER Christian Windolf <christianwindolf@web.de>

RUN apk update && \
  apk add postgresql-dev build-base && \
  pip install \
  Flask==0.12.2 \
  sqlalchemy==1.2.2 \
  geoalchemy2==0.4.2 \
  psycopg2==2.7.4 \
  urllib3==1.22 \
  gunicorn==19.7 && \
  apk del build-base

ENV BFB_DB_URL='postgresql://postgres:postgres@database:5432/battle_for_berlin'

WORKDIR /app

COPY *.py src/
COPY database/ ./src/database/



EXPOSE 8000

CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:8000", "src.app:app"]
