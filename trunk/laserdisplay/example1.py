#!/usr/bin/env python
# This example draws a dashed 2 color circle with increasing radius length
from LaserClient import *
import math

PI=3.1415
RED = [255,0,0]
GREEN = [0,255,0]

x=0x80
y=0x80
r=0x00

LD = LaserClient({"server":"localhost","port": 50000})

def draw_dashed_circle(x,y,r, c1, c2):
  step = 32
  for alpha in range(step):
    if alpha%2:
      LD.set_color(c1)
    else:
      LD.set_color(c2)
      
    LD.draw_line(x + r*math.cos(alpha*2*PI/step),
                 y + r*math.sin(alpha*2*PI/step),
                 x + r*math.cos((alpha+1)*2*PI/step),
                 y + r*math.sin((alpha+1)*2*PI/step))

while True:
  r+=1
  if r>0x100:
    r=0

  draw_dashed_circle(x, y, r, RED, GREEN)
  LD.show_frame()

