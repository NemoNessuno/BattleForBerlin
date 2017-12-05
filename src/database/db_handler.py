import os

from flask import json
from geoalchemy2 import functions
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URL = os.environ.get('BFB_DB_URL', 'postgresql://postgres:postgres@172.17.0.2:5432/battle_for_berlin')
engine = create_engine(DB_URL)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


# This is only here to have a crude method of simple testing
if __name__ == '__main__':
    from models import LetterDistrict, UrnDistrict

    labels = [
        "cdu", "spd", "gruene", "die_linke", "fdp", "afd"
    ]

    l_query = db_session.query(
        LetterDistrict.bwk,
        functions.ST_AsGeoJSON(functions.ST_Union(LetterDistrict.geom)).label("geom"),
        *[func.sum(getattr(LetterDistrict, label_name)).label(label_name) for label_name in labels]
    ).group_by(LetterDistrict.bwk)

    u_query = db_session.query(
        UrnDistrict.bwk,
        *[func.sum(getattr(UrnDistrict, label_name)).label(label_name) for label_name in labels]
    ).group_by(UrnDistrict.bwk)

    u_results = u_query.all()
    geojsons = []
    for row in l_query.all():
        geojson = json.loads(row.geom)
        u_result = next(x for x in u_results if lambda result: result.bwk == row.bwk)
        geojson["properties"] = {
            "bwk": row.bwk,
            "u_result": dict((label, getattr(u_result, label)) for label in labels),
            "l_result": dict((label, getattr(row, label)) for label in labels)
        }
        geojsons.append(geojson)

    print json.dumps(geojsons[0])
