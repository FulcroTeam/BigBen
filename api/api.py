from flask import Flask, request, jsonify, make_response, g
from binascii import hexlify
from hashlib import sha256, sha512
from pbkdf2 import PBKDF2
from os import urandom
import hmac
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = "database.db"

sessions = {}

def get_the_pepper():
    #Read the pepper from a file and delete the trailing newline
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


import serial
import time
from threading import Thread

class Arduino_one:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
        time.sleep(2)
        print("Comunicazione Seriale Aperta.")

    def serial_write_and_read(self, text=""):
        self.ser.write(text)
        self.ser.flush()
        time.sleep(0.2)
        char = self.ser.readline()[:-2] #no newlines
        print(char)
        return char

arduino_one = Arduino_one()
arduino_one.serial_write_and_read(b'digitalWrite;13;HIGH')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

#curl -d "username=castiglia.vincenzo&password=castix" http://localhost:8000/login
@app.route('/login', methods=['POST'])
def index():
    username = request.form.get('username')
    password = request.form.get('password')

    dbc = get_db().cursor()
    dbc.execute("SELECT key, salt, enabled FROM keys WHERE username = ?", (username,))
    fetched = dbc.fetchone()
    print("fetched from database: " + str(fetched))

    sessionid = ""

    if fetched != None:
        stored_key, salt, enabled = fetched
        if enabled:
            key_bytes = PBKDF2(password, salt, iterations=10000).read(32)
            pepper = get_the_pepper()
            final = hexlify(hmac.new(pepper, msg=key_bytes, digestmod=sha256).digest())

            if final == stored_key:
                sessionid = hexlify(urandom(32)).decode()
                sessions.update({ sessionid : { 'username' : username, 'timestamp' : datetime.utcnow() } })

    return jsonify({ 'sessionid' : sessionid})

#curl -d "sessionid=06b7b0fba14184b08cff926844752f99552e3d47f2aa9e0749ce2ae20f901211" http://localhost:8000/checklogin
@app.route('/checklogin', methods=['POST'])
def checklogin_route():
    sessionid = request.form.get('sessionid')
    logged = checklogin(sessionid)
    return jsonify({"logged" : logged})

def checklogin(sessionid):
    if sessionid in sessions:
        if sessions[sessionid]['timestamp'] > datetime.utcnow() - timedelta(minutes=5):
            sessions[sessionid]['timestamp'] = datetime.utcnow()
            return True
    return False

@app.route('/toggle13', methods=['POST', 'GET'])
def toggle13():
    if checklogin(request.form.get('sessionid')):
        status = bool(int(arduino_one.serial_write_and_read(b'toggle13;')))
        return jsonify({"logged" : True, "status" : status})
    return jsonify({"logged" : False})

"""
#parser queste sono cose tue... che devi farci?
ard = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
time.sleep(1)
print("Comunicazione Seriale Aperta.")

class CmdThread(threading.Thread):

    def __init__(self, ThreadId, actionCode):
        threading.Thread.__init__(self)
        self.ThreadId=ThreadId
        self.actionCode=actionCode

    def run(self):
        while True:
            onetoten = range(1, 4)
            for count in onetoten:
                ard.write(self.actionCode.encode())
            break

@app.route('/index', methods=['GET'])
def catchandshot():
    id = request.args.get('id')
    state = request.args.get('state')
    if(id=='condizionatore' and state=='on'):
      actionCode = '3'
    elif(id=='condizionatore' and state=='off'):
        actionCode = '4'
    print("id: "+id+"  -  state: "+state+"  -  actionCode: "+actionCode)
    ThreadGenerator(actionCode)
    return make_response(jsonify({'done': 'yes'}))

def ThreadGenerator(data):
    my_thread = CmdThread(0, data)
    my_thread.start()
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
