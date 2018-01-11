from flask import json
from geoalchemy2 import functions
from sqlalchemy import func

from db_handler import db_session
from models import MergedDistrictDiff, Diff, MergedDistrict, Candidate

PARTIES = [
    "cdu", "spd", "gruene", "die_linke", "fdp", "afd"
]


def get_district_geojson(district):
    query = db_session.query(district, functions.ST_AsGeoJSON(functions.ST_Transform(district.geom, 4326)))

    geojsons = []
    for district, geom in query.all():
        geojson = json.loads(geom)
        geojson["properties"] = district.get_geojson_dict()
        geojsons.append(geojson)

    return geojsons

def get_county_geojson():
#    l_query = db_session.query(
#        LetterDistrict.bwk,
#        functions.ST_AsGeoJSON(functions.ST_Union(LetterDistrict.geom)).label("geom"),
#        *sum_party_results(LetterDistrict)
#    ).group_by(LetterDistrict.bwk)
#
#    u_query = db_session.query(
#        UrnDistrict.bwk,
#        *sum_party_results(UrnDistrict)
#    ).group_by(UrnDistrict.bwk)
#
#    u_results = u_query.all()
#    u_dict = {r[0]: r for r in u_results}
#    geojsons = []
#    for row in l_query.all():
#        geojson = json.loads(row.geom)
#        u_result = u_dict[row.bwk]
#        geojson["properties"] = {
#            "bwk": row.bwk,
#            "u_result": dict((party, getattr(u_result, party)) for party in PARTIES),
#            "l_result": dict((party, getattr(row, party)) for party in PARTIES)
#        }

    query = db_session.query(
        MergedDistrictDiff.bwk,
        functions.ST_AsGeoJSON(functions.ST_Union(functions.ST_Transform(MergedDistrictDiff.geom, 4326))).label("geom"),
        *sum_party_results(MergedDistrictDiff)
    ).group_by(MergedDistrictDiff.bwk)

    geojsons = []
    for bwk, geom, cdu, spd, gruene, die_linke, fdp, afd in query.all():
        candidates = db_session.query(Candidate).filter(Candidate.bwk == bwk)
        geojson = json.loads(geom)
        geojson['properties'] = {
                'bwk': bwk,
                'candidates': {candidate.get_full_name(): candidate.get_json() for candidate in candidates},
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


def get_simplified_json(bwk):
    query = db_session.query(
        functions.ST_AsGeoJSON(functions.ST_Simplify(functions.ST_Union(MergedDistrict.geom), 0.001, True))
    ).filter(MergedDistrict.bwk == bwk)
    result = query.all()
    return list(result)[0]


def sum_party_results(model):
    return [func.sum(getattr(model, party)).label(party) for party in PARTIES]


def upsert_diff(identifier, bwk):
    diff = db_session.query(Diff).filter(Diff.identifier == identifier).first()
    diff = diff or Diff(identifier=identifier)
    diff.bwk = bwk
    db_session.add(diff)
    db_session.commit()


def truncate_diffs():
    db_session.execute('TRUNCATE TABLE diffs')
    db_session.commit()


def get_results():
    return {
        'real': get_results_from_table(MergedDistrict),
        'diff': get_results_from_table(MergedDistrictDiff)
    }


def get_results_from_table(table):
    query = db_session.query(
        table.bwk,
        *sum_party_results(table)
    ).group_by(table.bwk)
    result = {}
    for row in query.all():
        result[row[0]] = dict(zip(PARTIES, [int(p) for p in row[1:]]))
    return result
