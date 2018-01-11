#!/bin/sh

set -e

psql -U postgres < /data/database.sql
