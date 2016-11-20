"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver


import serial
import time
import threading



class CmdThread(threading.Thread):

    def __init__(self, ThreadId, codiceAzione):
        threading.Thread.__init__(self)
        self.ThreadId=ThreadId
        self.codiceAzione=codiceAzione

    def run(self):
        ard = serial.Serial('/dev/ttyACM0', 9600, timeout=0)
        print("Comunicazione Seriale Aperta.")
        while True:
            self.index+=1
            time.sleep(1)
            #x = ard.readline()
            ard.write(self.codiceAzione)
            #print("Message from arduino: ")
            #print(x)
            if(self.index==20):
                self._stop()





class S(BaseHTTPRequestHandler):


    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def do_GET(self):
        self._set_headers()
        self.wfile.write('<html> <body> <form method="post"> codice: <br> <input type="text" name="codice" value="(0-10)"> <br><br> <input type="submit" value="submit"> </form> </body> </html>'.encode())

    def do_HEAD(self):
        self._set_headers()


    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        post_dict = data_to_dict(post_data)

        codice_azione = str(post_dict[b'codice']).encode()
        self._set_headers()
        self.wfile.write(str(post_dict[b'codice']).encode())
        ThreadGenerator(codice_azione)
        #self.wfile.write(str(post_dict).encode())


def ThreadGenerator(data):
    my_thread = CmdThread(0, data)
    my_thread.start()



def data_to_dict(data):
    dictionary = {}
    key_and_value_list = data.split(b'&')
    for key_and_value in key_and_value_list:
        key_and_value = key_and_value.split(b'=')
        dictionary[key_and_value[0]] = key_and_value[1]
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