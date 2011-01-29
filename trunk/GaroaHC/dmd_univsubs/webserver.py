#!/usr/bin/python

ENABLE_TEXT_SCROLLING = chr(0)
DISABLE_TEXT_SCROLLING = chr(1)
SEND_GRAPHICS_BUFFER = chr(2)
SEND_LAMP_DATA = chr(3)
SEND_TEXT_MESSAGE = chr(4)
ONE_LINE_VERTICAL_CENTER = chr(5)
TWO_LINES_OF_TEXT = chr(6)

from unicodedata import normalize
import serial
ser = serial.Serial(port="/dev/ttyUSB0")
ser.setBaudrate(19200)

def sanitize(line):
  valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  newline = ""
  for c in normalize('NFKD', line.strip().decode("utf-8")).encode('ASCII','ignore').upper():
    if c in valid_chars:
      newline+=c
    else:
      newline+=" "
  return newline

last_text = ""
last_count = 0
def send_subtitle(text, counter):
  print "send_subtitle: ", text, counter
  global last_count, last_text

#  if counter<=last_count:
#    return

  if text == "" or text == last_text:
    return

  last_text = text
  last_count = counter

  if len(text)<=28:
    ser.write(ONE_LINE_VERTICAL_CENTER)
    send_text(sanitize(text),"")
  else:
    half = len(text)/2
    text = sanitize(text).split(" ")
    text1 = ""
    while len(text1)<half:
      text1 += text.pop(0) +" "
    text2 = " ".join(text)
    ser.write(TWO_LINES_OF_TEXT)
    send_text(text1, text2)
  
def send_text(msg1, msg2):
  ser.write(DISABLE_TEXT_SCROLLING)

  msg1 = '{0:^28}'.format(msg1)
  msg2 = '{0:^28}'.format(msg2)

  print "\nmsg1:"+msg1
  print "msg2:"+msg2

  print "len(msg1):",len(msg1)
  print "len(msg2):",len(msg2)
  
  ser.write(SEND_TEXT_MESSAGE)
  ser.write(msg1)
  ser.write(msg2)
  
import urllib
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
class MyHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    try:
      if "?" in self.path:
        params = urllib.unquote(self.path.split("?")[1])
        if "&" in params:
          text, counter = params.split("&")
          send_subtitle(text, counter)
        else:
          return

      return
            
    except IOError:
	    self.send_error(404,'File Not Found: %s' % self.path)
     
def main():
	try:
		server = HTTPServer(('', 8080), MyHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
		server.socket.close()
		ser.close()			# fecha a porta

if __name__ == '__main__':
  main()

