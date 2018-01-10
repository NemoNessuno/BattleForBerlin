FROM python:2.7

MAINTAINER Christian Windolf <christianwindolf@web.de>

ENV BFB_DB_URL='postgresql://postgres:postgres@database:5432/battle_for_berlin'

WORKDIR /app

COPY *.py requirements.txt ./
COPY database/ database/

RUN pip install -r requirements.txt && pip install gunicorn

EXPOSE 8000

CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
