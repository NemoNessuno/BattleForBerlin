from flask import Flask, render_template, jsonify, request, Response
import requests

from database.models import (
    MergedDistrict,
    MergedDistrictDiff,
    Diff
    )

from database.db_helper import (
    get_district_geojson,
    get_county_geojson,
    upsert_diff,
    get_simplified_json,
    truncate_diffs
)

from database.db_handler import db_session

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html')


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

@app.route('/api/diff/count', methods=['GET'])
def get_diff_count():
    return jsonify({'count': int(db_session.query(Diff.bwk).count())})

@app.route('/api/county/<countyid>')
def simple_county(countyid):
    return get_simplified_json(countyid)


@app.route('/api/diff/create', methods=['POST'])
def create_diff():
    payload = request.get_json()
    upsert_diff(payload['identifier'], payload['bwk'])
    return jsonify({'msg': 'district changed'})

@app.route('/api/candidate/<candidate>', methods=['GET'])
def proxy_candidate(candidate):
    payload = requests.get('https://www.abgeordnetenwatch.de/api/parliament/bundestag/profile/%s/profile.json' % candidate)
    resp = Response(payload)
    resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
