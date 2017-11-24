# BattleForBerlin
A GIS application inteded to show the effects of Gerrymandering on the Bundestagswahl 2017

## Getting started

Before you start, please make sure the following is installed on
your machine:

* Python 2.7
* Node 8.9 or higher (and yarn package manager)
* Postgres 9.5/PostGIS 2.4 *(in the following guide it will be set up via docker)*

You can install the Postgres/PostGIS via package management of
your Linux distribution, or just use docker (and all your wishes come true :) )
If you omit the password in the `docker run` command, then
the password will be `postgres`.
```bash
docker run \
  --detach \
  -p 127.0.0.1:5432:5432 \
  --name postgis \
  -e POSTGRES_PASSWORD=<secret password> \
  --restart always \
  mdillon/postgis:9.5

echo 'create database battle_for_berlin;' | psql -U postgres -h localhost
psql -U postgres -h localhost < /path/to/sql/dump.sql
```

Next step is to start the backend.
```bash
cd ./src
pip install -r requirements.txt
export FLASK_DEBUG=1
export FLASK_APP=app.py

# * if your postgis is not on localhost or password is not postgres
# * provide sqlalchemy compatible database url
export BFB_DB_URL='postgres://user:password@hostname/db_name'
flask run #will block your terminal
```

And finally the shiny frontend:
```bash
cd ./frontend
yarn # or npm i
yarn dev # or npm run dev
```

Open your browser at `localhost:8080` and have fun!
