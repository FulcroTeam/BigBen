from flask import Flask, request, jsonify, make_response
from binascii import hexlify, unhexlify
from pbkdf2 import PBKDF2
from os import urandom
import hmac
import pyaes
import datetime
import sqlite3

app = Flask(__name__)

import serial
import time
import threading

ard = serial.Serial('/dev/ttyACM1', 9600, timeout=0)
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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/login', methods=['POST'])
def index():
    username = request.form.get('username')
    password = request.form.get('password')

    dbc = sqlite3.connect('database.db').cursor()
    dbc.execute("SELECT key, salt, enabled FROM keys WHERE username = ?", (username,))
    fetched = dbc.fetchone()
    print("fetched from database: " + str(fetched))

    sessionid = ""

    if fetched != None:
        stored_key, salt, enabled = fetched
        if enabled:
            pbkdf2_key = PBKDF2(password, salt, iterations=10000)
            calculated_key = pbkdf2_key.hexread(32)
            calculated_key_bytes = pbkdf2_key.read(32)
            print("calculated_key:" + calculated_key)
            if calculated_key == stored_key:
                counter_bytes = urandom(16)
                counter = pyaes.Counter(initial_value = int.from_bytes(counter_bytes, byteorder='big'))
                aes = pyaes.AESModeOfOperationCTR(calculated_key_bytes, counter)
                sessionid = hexlify(counter_bytes).decode() + '|' + str(datetime.datetime.utcnow()) + '|' + username
                print("unencrypted sessionid: " + sessionid)
                ciphertext = aes.encrypt(sessionid)
                sessionid = hexlify(ciphertext).decode()
                print("encrypted sessionid: " + sessionid)

    return jsonify({ 'sessionid' : sessionid})


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
