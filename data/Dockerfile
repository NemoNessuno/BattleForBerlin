FROM mdillon/postgis:9.5

MAINTAINER Christian Windolf <christianwindolf@web.de>

WORKDIR /data

COPY database.tar.gz extensions.sql ./

RUN mkdir -p /docker-entrypoint-initdb.d/ && \
  tar xf database.tar.gz

COPY battleforberlin.sh /docker-entrypoint-initdb.d/z-10-init-db.sh
