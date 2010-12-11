#!/usr/bin/env python
# This example draws a dashed 2 color circle with increasing radius length
from LaserDisplay import LaserDisplay

x=0x80
y=0x80
r=0x00
c1 = [0xFF,0x00,0x00] #red
c2 = [0x00,0xFF,0x00] #green

LD = LaserDisplay()
while True:
  r+=1
  if r>0x100:
    r=0
  LD.draw_dashed_circle(x, y, r, c1, c2)

