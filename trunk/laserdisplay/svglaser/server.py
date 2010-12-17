#!/usr/bin/python

import BaseHTTPServer

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        if self.headers.has_key('content-length'):
            length= int( self.headers['content-length'] )
            svg = self.rfile.read(length)
            print svg

        self.send_response(200)
        self.end_headers()

server_address = ('', 8000)
httpd = BaseHTTPServer.HTTPServer(server_address, MyHandler)

print 'listening at 8000 ...'

while True:
    httpd.handle_request()
