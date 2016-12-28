from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import socketserver
import sqlite3
import json


class S(BaseHTTPRequestHandler):

    #test it with 
    #curl -d "" localhost:8000
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        #username = "sergio.parisi"
        #pin = "1234"

        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        post_dict = data_to_dict(post_data)

        print(json.dumps(post_dict))


        username = str(post_dict['username'])
        pin = str(post_dict['pin'])


        print(username)
        print(pin)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT CASE WHEN EXISTS (SELECT * FROM lista_chiavi WHERE nome_utente = ? AND pin = ?) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END", (username, pin))
        a = c.fetchone()
        data = {
            'response' : a[0]
        }
        print(a)
        self.wfile.write(str(json.dumps(data, indent=4)).encode())


def data_to_dict(data):
    dictionary = {}
    key_and_value_list = data.split(b'&')
    for key_and_value in key_and_value_list:
        key_and_value = key_and_value.split(b'=')
        dictionary[key_and_value[0].decode('utf-8')] = key_and_value[1].decode('utf-8')
    return dictionary

def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()