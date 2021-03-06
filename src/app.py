from Queue import Queue

from flask import Flask, render_template, jsonify, request, Response

from database.models import (
    MergedDistrict,
    MergedDistrictDiff,
    Diff
    )

from database.db_helper import (
    get_district_geojson,
    get_county_geojson,
    upsert_diff,
    truncate_diffs
)

from database.db_handler import db_session
from src.database.gerrymandering_algorithm import GerrymanderingThread
from src.database.gerrymandering_helper import GerrymanderingQueue

app = Flask(__name__)
# pipe curl into jq if you need a pretty printed result
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
gerrymandering_thread = None


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


@app.route('/api/diff/create', methods=['POST'])
def create_diff():
    payload = request.get_json()
    upsert_diff(payload['identifier'], payload['bwk'])
    return jsonify({'msg': 'district changed'})



@app.route('/api/gerrymander', methods=['POST'])
def gerrymander():
    global gerrymandering_thread
    if gerrymandering_thread:
        return jsonify({'error': 'There is already a gerrymandering process running at the time'}), 423
    else:
        parameter = request.get_json()
        gerrymandering_thread = GerrymanderingThread(bwk=parameter['bwk'], party=parameter['party'],
                                                     queue=GerrymanderingQueue(Queue()))
        gerrymandering_thread.start()
        return jsonify({'status': 'calculation initialized'})


@app.route('/api/gsteps', methods=['GET'])
def get_gerrymander_steps():
    global gerrymandering_thread
    if gerrymandering_thread:
        result = gerrymandering_thread.queue.get_all()
        if not gerrymandering_thread.isAlive():
            # make sure we append all the stuffs
            result += gerrymandering_thread.queue.get_all()
            gerrymandering_thread = None
        return jsonify(result)
    else:
        return jsonify({'error': 'No gerrymandering process running at the moment'}), 404

@app.after_request
def close_session(response):
    db_session.commit()
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
