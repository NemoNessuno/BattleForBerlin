from flask import json
from geoalchemy2 import functions
from sqlalchemy import func

from db_handler import db_session
from models import LetterDistrict, UrnDistrict

PARTIES = [
    "cdu", "spd", "gruene", "die_linke", "fdp", "afd"
]


def get_district_geojson(district):
    query = db_session.query(district, functions.ST_AsGeoJSON(district.geom))

    geojsons = []
    for district, geom in query.all():
        geojson = json.loads(geom)
        geojson["properties"] = district.get_geojson_dict()
        geojsons.append(geojson)

    return geojsons


def get_county_geojson():
    l_query = db_session.query(
        LetterDistrict.bwk,
        functions.ST_AsGeoJSON(functions.ST_Union(LetterDistrict.geom)).label("geom"),
        *sum_party_results(LetterDistrict)
    ).group_by(LetterDistrict.bwk)

    u_query = db_session.query(
        UrnDistrict.bwk,
        *sum_party_results(UrnDistrict)
    ).group_by(UrnDistrict.bwk)

    u_results = u_query.all()
    u_dict = {r[0]:r for r in u_results}
    geojsons = []
    for row in l_query.all():
        geojson = json.loads(row.geom)
        u_result = u_dict[row.bwk]
        geojson["properties"] = {
            "bwk": row.bwk,
            "u_result": dict((party, getattr(u_result, party)) for party in PARTIES),
            "l_result": dict((party, getattr(row, party)) for party in PARTIES)
        }
        geojsons.append(geojson)

    return geojsons

def sum_party_results(model):
    return [func.sum(getattr(model, party)).label(party) for party in PARTIES]
