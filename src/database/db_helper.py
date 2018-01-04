from flask import json
from geoalchemy2 import functions
from sqlalchemy import func

from db_handler import db_session
from models import LetterDistrict, UrnDistrict


def get_district_geojson(district):
    query = db_session.query(district, functions.ST_AsGeoJSON(district.geom))

    geojsons = []
    for district, geom in query.all():
        geojson = json.loads(geom)
        geojson["properties"] = district.get_geojson_dict()
        geojsons.append(geojson)

    return geojsons


def get_county_geojson():
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

        for loc_u_result in u_results:
            if loc_u_result.bwk == row.bwk:
                u_result = loc_u_result
                break

        geojson["properties"] = {
            "bwk": row.bwk,
            "u_result": dict((label, getattr(u_result, label)) for label in labels),
            "l_result": dict((label, getattr(row, label)) for label in labels)
        }

        geojsons.append(geojson)

    return geojsons
