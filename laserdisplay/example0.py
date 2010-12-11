#!/usr/bin/env python
# simple line animation
from LaserDisplay import *

#LD = LaserDisplay()
LD = LaserDisplay({"server":"localhost","port": 50000})

y=0
while True:
  y += 1
  if y > 255:
    y=0
  LD.draw_line(0, 0, 0, y)
  LD.show_frame()

