#!/usr/bin/env python
from LaserDisplay import *
import math
import random

WIDTH = 100
HEIGHT = 100

LD = LaserDisplay()

ship = [[190, 64], [168, 136], [118, 200], [77, 142], [63, 63], [87, 77], [105, 103], [119, 114], [143, 104], [158, 81], [192, 63]]

cx,cy = WIDTH/2, HEIGHT/2

angle=0
while True:
    angle+=0.01
    LD.save()
    LD.scale(0.2)
    LD.rotate_at(cx,cy,angle)
    LD.set_color(RED)
    LD.draw_bezier(ship, 10)
    LD.translate(10,0)
    LD.set_color(GREEN)
    LD.draw_bezier(ship, 10)
    LD.restore()
    
    
    LD.save()
    LD.scale(0.4)
    LD.rotate_at(cx,cy,angle+2*PI*0.4)

    LD.translate(30,50)
    LD.set_color(RED)
    LD.draw_bezier(ship, 10)

    LD.translate(30,0)
    LD.set_color(GREEN)
    LD.draw_bezier(ship, 10)
    LD.restore()
    
    
    


