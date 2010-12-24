#!/usr/bin/env python
# simple line animation
from LaserClient import *

LD = LaserClient({"server":"localhost","port": 50000})
LD.set_scan_rate(35000)

y=0
while True:
  y += 1
  if y > 255:
    y=0
  LD.draw_line(128, 0, 128, y)
  LD.show_frame()

