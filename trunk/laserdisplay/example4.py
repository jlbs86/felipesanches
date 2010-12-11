#!/usr/bin/env python
# A clock!
from LaserDisplay import *
import math
import random

WIDTH = 255
HEIGHT = 255

#LD = LaserDisplay()
LD = LaserDisplay({"server":"localhost"})

import time
while True:
  t = time.localtime()
  
  hours = t.tm_hour%12
  minutes = t.tm_min
  seconds = t.tm_sec

  LD.set_color(RED)
#  LD.draw_text("%02i:%02i:%02i"%(hours,minutes,seconds), 220, 220, 20)

  LD.set_color(BLUE)
  angle = 2*PI*seconds/60 + PI/2
  r = 2.0/3 * (WIDTH/2)
  LD.draw_line(WIDTH/2, HEIGHT/2, WIDTH/2 + r*math.cos(angle), HEIGHT/2 + r*math.sin(angle))

  LD.set_color(MAGENTA)
  angle = 2*PI*minutes/60 + 2*PI/60 * float(seconds)/60 + PI/2
  LD.draw_line(WIDTH/2, HEIGHT/2, WIDTH/2 + r*math.cos(angle), HEIGHT/2 + r*math.sin(angle))

  angle = 2*PI*hours/12 + 2*PI*minutes/(60*12) + PI/2
  r *= 2.0/3
  LD.draw_line(WIDTH/2, HEIGHT/2, WIDTH/2 + r*math.cos(angle), HEIGHT/2 + r*math.sin(angle))

  r1 = 2.0/3 * (WIDTH/2)
  r2 = 1.9/3 * (WIDTH/2)

  LD.set_color(RED)
  for i in range(12):
    angle = i * 2*PI/12
    LD.draw_line(WIDTH/2 + r1*math.cos(angle), HEIGHT/2 + r1*math.sin(angle), WIDTH/2 + r2*math.cos(angle), HEIGHT/2 + r2*math.sin(angle))

  LD.show_frame()
