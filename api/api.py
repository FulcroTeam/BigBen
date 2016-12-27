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
        
        username = "sergio.parisi"
        pin = "1234"
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT CASE WHEN EXISTS (SELECT * FROM lista_chiavi WHERE nome_utente = ? AND pin = ?) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END", (username, pin))
        data = {
            'logged' : c.fetchone()[0]
        }
        
        self.wfile.write(str(json.dumps(data, indent=4)).encode())



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