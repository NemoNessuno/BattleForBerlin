import json
from flask import Flask, render_template, jsonify
from geoalchemy2 import functions

from database.db_handler import db_session
from database.models import LetterDistrict, UrnDistrict

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/api/districts/ballot')
def urn_districts():
    return jsonify(get_geojson(db_session.query(UrnDistrict, functions.ST_AsGeoJSON(UrnDistrict.geom))))


@app.route('/api/districts/letters')
def letter_districts():
    return jsonify(get_geojson(db_session.query(LetterDistrict, functions.ST_AsGeoJSON(LetterDistrict.geom))))

def get_geojson(query):
    geojsons = []
    for district, geom in query.all():
        geojson = json.loads(geom)
        geojson["properties"] = district.get_geojson_dict()
        geojsons.append(geojson)

    return geojsons


if __name__ == '__main__':
    app.debug = True
    app.run()
