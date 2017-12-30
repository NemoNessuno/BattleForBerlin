from flask import json
from geoalchemy2 import functions
from sqlalchemy import func

from db_handler import db_session
from models import MergedDistrict

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
    query = db_session.query(
        MergedDistrict.bwk,
        functions.ST_AsGeoJSON(functions.ST_Union(MergedDistrict.geom)).label("geom"),
        *sum_party_results(MergedDistrict)
    ).group_by(MergedDistrict.bwk)

    geojsons = []
    for bwk, geom, cdu, spd, gruene, die_linke, fdp, afd in query.all():
        geojson = json.loads(geom)
        geojson['properties'] = {
                'bwk': bwk,
                'result': {
                    'cdu': int(cdu),
                    'spd': int(spd),
                    'gruene': int(gruene),
                    'die_linke': int(die_linke),
                    'fdp': int(fdp),
                    'afd': int(afd)
                    }
                }
        geojsons.append(geojson)

    return geojsons

def sum_party_results(model):
    return [func.sum(getattr(model, party)).label(party) for party in PARTIES]
