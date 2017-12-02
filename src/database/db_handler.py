from flask import json
import os
from geoalchemy2 import functions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URL = os.environ.get('BFB_DB_URL', 'postgresql://postgres:postgres@172.17.0.2:5432/battle_for_berlin')
engine = create_engine(DB_URL)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# This is only here to have a crude method of simple testing
if __name__ == '__main__':
    from models import LetterDistrict

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.
    query = db_session.query(LetterDistrict, functions.ST_AsGeoJSON(LetterDistrict.geom))
    geojsons = []
    for district, geom in query.all():
        geojson = json.loads(geom)
        geojson["properties"] = district.get_geojson_dict()
        geojsons.append(geojson)

    print json.dumps(geojsons[0:1])

