#!/bin/sh

set -e

echo 'create database battle_for_berlin;' | psql -U postgres
psql -U postgres -d battle_for_berlin < /data/database.sql
psql -U postgres -d battle_for_berlin < /data/extensions.sql
