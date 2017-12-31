import json
from flask import Flask, render_template, jsonify

from database.models import LetterDistrict, UrnDistrict, MergedDistrict, MergedDistrictDiff
from database.db_helper import get_district_geojson, get_county_geojson

app = Flask(__name__)

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/api/districts/ballot')
def urn_districts():
    return jsonify(get_district_geojson(UrnDistrict))


@app.route('/api/districts/letters')
def letter_districts():
    return jsonify(get_district_geojson(LetterDistrict))

@app.route('/api/districts/merged')
def merged_districts():
    return jsonify(get_district_geojson(MergedDistrict))

@app.route('/api/districts/merged_diff')
def merged_districts_diff():
    return jsonify(get_district_geojson(MergedDistrictDiff))

@app.route('/api/counties')
def counties():
    return jsonify(get_county_geojson())

if __name__ == '__main__':
    app.debug = True
    app.run()
