from flask import Flask, render_template, jsonify, json
from geoalchemy2 import functions

from database.db_handler import db_session
from database.models import District

app = Flask(__name__)


@app.route('/')
def start():

    return render_template('index.html', shapes=map(json.dumps, get_districts()))


# Returns district shapes
def get_districts():
    return db_session.query(functions.ST_AsGeoJSON(functions.ST_Transform(District.geom, 4326))).all()

if __name__ == '__main__':
    app.debug = True
    app.run()
