import os
import bcrypt
from flask import Flask, session, render_template, request, redirect

def get_hash():
    filename = os.environ.get('HASH_FILE', './hash.txt')
    with open(filename, 'rb') as stream:
        return stream.read()

app = Flask(__name__)
app.secret_key = 'randomstring'

HASH = get_hash()

@app.route('/auth/authorized')
def authorized():
    if session.get('authenticated'):
        return 'OK', 202
    return 'NOT AUTHORIZED', 401

@app.route('/auth/login', methods=['GET'])
def get_login_form():
    return render_template('login.html')

@app.route('/auth/authenticate', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    host = request.host
    proto = 'http' if os.environ.get('FLASK_DEBUG') == 1 else 'https'
    base = proto + '://' + host
    if username == 'sudo' and bcrypt.checkpw(bytes(password, 'utf8'), HASH):
        session['authenticated'] = True
        return redirect(base + '/')
    return redirect(base + '/auth/login')
