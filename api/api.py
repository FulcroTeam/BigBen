from flask import Flask, request, jsonify, make_response
from binascii import hexlify
from pbkdf2 import PBKDF2
from os import urandom
import sqlite3

app = Flask(__name__)
app.secret_key = 'stringa segreta dell\'api'

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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/login', methods=['POST'])
def index():
    username = request.form.get('username')
    password = request.form.get('password')
    print(username)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT key, salt, enabled FROM keys WHERE username = ?", (username,))
    a = c.fetchone()
    print(a)

    sessionid = ""

    return jsonify({ 'sessionid' : sessionid})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
