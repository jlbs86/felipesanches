#!/usr/bin/env python
from LaserDisplay import *
import math
import random

WIDTH = 255
HEIGHT = 255
RED = [255,0,0]
LD = LaserDisplay()

import time
while True:
  t = time.localtime()
  
  hours = t.tm_hour
  minutes = t.tm_min
  seconds = t.tm_sec

  LD.set_color(RED)
  LD.draw_text("%02i:%02i:%02i"%(hours,minutes,seconds), 220, 220, 20)

  angle = 2*PI*seconds/60 + PI/2
  r = 2.0/3 * (WIDTH/2)
  LD.draw_line(WIDTH/2, HEIGHT/2, WIDTH/2 + r*math.cos(angle), HEIGHT/2 + r*math.sin(angle))

  angle = 2*PI*minutes/60 + PI/2
  LD.draw_line(WIDTH/2, HEIGHT/2, WIDTH/2 + r*math.cos(angle), HEIGHT/2 + r*math.sin(angle))

  angle = 2*PI*hours%12/12 + angle/12 + PI/2
  r *= 2.0/3
  LD.draw_line(WIDTH/2, HEIGHT/2, WIDTH/2 + r*math.cos(angle), HEIGHT/2 + r*math.sin(angle))

