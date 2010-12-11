#!/usr/bin/env python
# This example draws a dashed 2 color circle with increasing radius length
from LaserDisplay import *

x=0x80
y=0x80
r=0x00

#LD = LaserDisplay()
LD = LaserDisplay({"server":"localhost","port": 50000})

while True:
  r+=1
  if r>0x100:
    r=0

  LD.draw_dashed_circle(x, y, r, RED, GREEN)
  LD.show_frame()

