import json
from flask import Flask, render_template, jsonify, request

from database.models import (
    LetterDistrict,
    UrnDistrict,
    MergedDistrict,
    MergedDistrictDiff)

from database.db_helper import (
    get_district_geojson,
    get_county_geojson,
    upsert_diff,
    get_simplified_json,
    get_results,
    truncate_diffs
)

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

@app.route('/api/diff/reset', methods=['POST'])
def reset():
    truncate_diffs()
    return jsonify({'msg': 'diffs deleted'})

@app.route('/api/county/<countyid>')
def simple_county(countyid):
    return get_simplified_json(countyid)

@app.route('/api/diff/create', methods=['POST'])
def create_diff():
    payload = request.get_json()
    upsert_diff(payload['identifier'], payload['bwk'])
    return jsonify({'msg': 'district changed'})

@app.route('/api/results')
def results():
    return jsonify(get_results())

if __name__ == '__main__':
    app.debug = True
    app.run()
