from flask import Flask, Response
import requests

app = Flask(__name__)

PROFILE_TEMPLATE = 'https://www.abgeordnetenwatch.de/api/parliament/bundestag/profile/%s/profile.json'

@app.route('/api/candidate/<candidate>', methods=['GET'])
def proxy_candidate(candidate):
    payload = requests.get(PROFILE_TEMPLATE % candidate)
    resp = Response(payload)
    resp.headers['Content-Type'] = 'application/json'
    return resp
