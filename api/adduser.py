#!/usr/bin/python3
from binascii import hexlify
from hashlib import sha256
from pbkdf2 import PBKDF2
from os import urandom
import sqlite3
import hmac
import sys

def main(argv):
    if len(argv) != 3:
        sys.stderr.write("USAGE: you have to pass two parameters:\n")
        sys.stderr.write("1) Username\n")
        sys.stderr.write("2) Password\n")
        sys.stderr.write("The order matters!\n")
        sys.stderr.write("The user would be directely inserted into database.db\n")
        return 1
    else:
        #Read the pepper from a file and delete the trailing newline
        pepper_f = open('pepper', 'r')
        pepper = pepper_f.readline()[:-1].encode()
        pepper_f.close()

        #Generate random salt
        salt = hexlify(urandom(8))

        #Generate the key using password and salt
        pbkdf2 = PBKDF2(argv[2], salt, iterations=10000)
        key_b = pbkdf2.read(32)
        key = pbkdf2.hexread(32)

        #Add the pepper
        final = hexlify(hmac.new(pepper, msg=key_b, digestmod=sha256).digest())


        print("pepper: " + pepper.decode())
        print("salt: " + salt.decode())
        print("username: " + argv[1])
        print("password: " + argv[2])
        print("key: " + key)
        print("final: " + final.decode())

        db = sqlite3.connect('database.db')
        dbc = db.cursor()
        dbc.execute("INSERT INTO keys VALUES (NULL, ?, ?, ?, 'true')", (argv[1], final, salt,))
        db.commit()
        db.close()

        print("OK. User added")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
