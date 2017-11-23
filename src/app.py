from flask import Flask, render_template, jsonify, json, Response
from geoalchemy2 import functions

from database.db_handler import db_session
from database.models import District

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('index.html')


# Returns district shapes
@app.route('/districts')
def get_districts():
    resp = Response("[" + ",".join([x[0] for x in db_session.query(functions.ST_AsGeoJSON(functions.ST_Transform(District.geom, 4326))).all()]) + "]")
    resp.headers["Content-Type"]="app/json"

    return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
