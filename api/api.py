from flask import Flask, request, jsonify, make_response, g
from binascii import hexlify
from hashlib import sha256, sha512
from pbkdf2 import PBKDF2
from os import urandom
import hmac
from datetime import datetime, timedelta
import sqlite3
import serial
import time


from threading import Thread


app = Flask(__name__)
app.config['DATABASE'] = "database.db"
app.config['DEBUG'] = True


sessions = {}


def get_the_pepper():
    # Read the pepper from a file and delete the trailing newline
    pepper_f = open('pepper', 'r')
    pepper = pepper_f.readline()[:-1].encode()
    pepper_f.close()
    return pepper


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


class Arduino_one:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
        time.sleep(2)
        print("Comunicazione Seriale Aperta.")

    def serial_write_and_read(self, text=""):
        self.ser.write(text)
        self.ser.flush()
        time.sleep(0.2)
        char = self.ser.readline()[:-2]  # no newlines
        app.logger.debug("arduino char: " + str(char))
        return char


arduino_one = Arduino_one()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# curl -d "username=castiglia.vincenzo&password=castix"
# http://localhost:8000/login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    dbc = get_db().cursor()
    dbc.execute("SELECT key, salt FROM users WHERE username = ?",
                (username,))
    fetched = dbc.fetchone()
    print("fetched from database: " + str(fetched))

    sessionid = ""

    if fetched is not None:
        stored_key, salt = fetched

        key_bytes = PBKDF2(password, salt, iterations=10000).read(32)
        pepper = get_the_pepper()
        final = hexlify(hmac.new(pepper, msg=key_bytes, digestmod=sha256).
                        digest())

        if final == stored_key:
            sessionid = hexlify(urandom(32)).decode()
            sessions.update({sessionid: {
                'username': username,
                'timestamp': datetime.utcnow()
                }})

    return jsonify({'sessionid': sessionid})


# curl -d "sessionid=bfdkabfkb...asdbfiusadbi" http://localhost:8000/checklogin
@app.route('/checklogin', methods=['POST'])
def checklogin_route():
    sessionid = request.form.get('sessionid')
    logged = checklogin(sessionid)
    return jsonify({"logged": logged})


def checklogin(sessionid):
    if sessionid in sessions:
        if sessions[sessionid]['timestamp'] > datetime.utcnow() - timedelta(
                minutes=10):
            sessions[sessionid]['timestamp'] = datetime.utcnow()
            return True
    return False

"""
@app.route('/toggle/<int:pin>', methods=['POST', 'GET'])
def toggle(pin):
    if checklogin(request.form.get('sessionid')):
        print("pin:" + pin)
        status = bool(int(
            arduino_one.serial_write_and_read(b'toggle;' + str(pin).encode())))
        return jsonify({"logged": True, "status": status})
    return jsonify({"logged": False})


@app.route('/temperature/<string:pin>', methods=['POST', 'GET'])
def temperature(pin):
    if checklogin(request.form.get('sessionid')):
        temperature = float(
            arduino_one.serial_write_and_read(
                b'temperature;' + str(pin).encode()))
        # print(float(arduino_one.serial_write_and_read(
        # b'temperature;' + str(pin).encode())))
        return jsonify({"logged": True, "temperature": temperature})
    return jsonify({"logged": False})
"""

@app.route('/', methods=['POST'])
def index():
    if checklogin(request.form.get('sessionid')):
        response_data = {"logged": True}
        command = request.form.get('command')
        pin = request.form.get('pin')
        value = request.form.get('value')
        if command == 'toggle':
            response_data['on'] = bool(int(
                arduino_one.serial_write_and_read(
                    b'toggle;' + str(pin).encode())))

        elif command == 'temperature':
            response_data['temperature'] = float(
                arduino_one.serial_write_and_read(
                    b'temperature;' + str(pin).encode()))
            print(response_data['temperature'])

        else:
            response_data['error'] = "COMMAND UNRECOGNIZED: " + command

        return jsonify(response_data)

    return jsonify({"logged": False})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
