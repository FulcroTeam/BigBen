from flask import Flask, request, jsonify, make_response
from binascii import hexlify, unhexlify
from pbkdf2 import PBKDF2
from os import urandom
import hmac
import pyaes
import datetime
import sqlite3

app = Flask(__name__)

# TODO
# To generate a new user key:
# salt = hexlify(urandom(8)) #64 bit salt
# key = PBKDF2("newpassword", salt, iterations=10000).hexread(32)
# change hexread() with read to get the bytes instead of the hex
# then store both password and salt in the database
# REAL EXAMPLE:
"""Python 3.5.2+ (default, Nov 22 2016, 01:00:20)
[GCC 6.2.1 20161119] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from binascii import hexlify
>>> from pbkdf2 import PBKDF2
>>> from os import urandom
>>> salt = hexlify(urandom(8))
>>> password = "1234"
>>> key = PBKDF2(password, salt, iterations=10000).hexread(32)
>>> key
'a2147ef91cd3843269f6f74317afd540ddfaf346699b0578434c87b31ce2ded6'
>>>
"""
# TODO SECURITY UPGRADE
# i also want the pepper
"""
import hmac
from hashlib import sha256
password = b'password'
pepper = b'secret pepper'
dig = hmac.new(pepper, msg=password, digestmod=sha256).digest()
hexlify(dig)
"""


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
