#!/usr/bin/env python
from LaserDisplay import *

LD = LaserDisplay({"server":"localhost","port": 50000})
#LD = LaserDisplay()

import sys
filename = sys.argv[1]

from xml.sax import make_parser
from xml.sax.handler import ContentHandler 

class SVGHandler(ContentHandler):
  def startElement(self, name, attrs):
    if name=="path":
      tokens = attrs.get('d').split(" ")
      i=0
      x,y=0,0
      x0,y0=x,y
      
      while i<len(tokens):
        if tokens[i].lower() in ["m", "c", "l", "h", "v", "z"]:
          cmd = tokens[i]
          i+=1
        
        if cmd=="m":
          delta=tokens[i].split(",")
          x+=float(delta[0])
          y+=float(delta[1])
          x0,y0=x,y
          cmd="l"
        elif cmd=="M":
          delta=tokens[i].split(",")
          x=float(delta[0])
          y=float(delta[1])
          x0,y0=x,y
          cmd="l"
        elif cmd=="l":
          delta=tokens[i].split(",")
          LD.draw_line(x,y,x+float(delta[0]),y+float(delta[1]))
          x+=float(delta[0])
          y+=float(delta[1])
        elif cmd=="L":
          delta=tokens[i].split(",")
          LD.draw_line(x,y,float(delta[0]),float(delta[1]))
          x=float(delta[0])
          y=float(delta[1])
        elif cmd=="z" or cmd=="Z":
          i-=1
          LD.draw_line(x,y,x0,y0)
          x,y=x0,y0
        elif cmd=="h":
          delta=tokens[i]
          LD.draw_line(x,y,x+float(delta),y)
          x+=delta
        elif cmd=="H":
          delta=tokens[i]
          LD.draw_line(x,y,float(delta),y)
          x=delta
        elif cmd=="v":
          delta=tokens[i]
          LD.draw_line(x,y,x,y+float(delta))
          y+=delta
        elif cmd=="V":
          delta=tokens[i]
          LD.draw_line(x,y,x,float(delta))
          y=delta
        elif cmd=="c":
          ctrl1=tokens[i].split(",")
          ctrl2=tokens[i+1].split(",")
          delta=tokens[i+2].split(",")
          LD.draw_cubic_bezier([[x,y],[x+float(ctrl1[0]),y+float(ctrl1[1])],[x+float(ctrl2[0]),y+float(ctrl2[1])],[x+float(delta[0]),y+float(delta[1])]],15)
          x+=float(delta[0])
          y+=float(delta[1])
          i+=2
        elif cmd=="C":
          ctrl1=tokens[i].split(",")
          ctrl2=tokens[i+1].split(",")
          delta=tokens[i+2].split(",")
          LD.draw_cubic_bezier([[x,y],[float(ctrl1[0]),float(ctrl1[1])],[float(ctrl2[0]),float(ctrl2[1])],[float(delta[0]),float(delta[1])]],15)
          x+=float(delta[0])
          y+=float(delta[1])
          i+=2
        i+=1

#we want to parse this: <path d=""/>
parser = make_parser()   
parser.setContentHandler(SVGHandler())
parser.parse(open(filename))

mess = LD.messageBuffer
LD.set_scan_rate(35000)
LD.set_blanking_delay(0)

while True:
    LD.messageBuffer = mess
    LD.show_frame()
