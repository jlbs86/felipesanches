#!/usr/bin/env python
from LaserDisplay import *
import math
import random

WIDTH = 255
HEIGHT = 255

NUM_POINTS = 10
NUM_SHAPES = 2
PI = 3.1415
MAXSPEED = 8
NOISE = 0
PROBAB_COLOR_CHANGE=0.05
COLOR_CHANGE_MAXSTEP = 256


class Particle:
  def __init__(self, display):
    self.d = display
    self.reset()
    self.color = [int(int(random.random()*4)*255/4),int(int(random.random()*4)*255/4),int(int(random.random()*4)*255/4)]
    
  def reset(self):
    self.r = 1
    self.x = random.random()*(WIDTH-2*self.r) + self.r
    self.y = random.random()*(HEIGHT-2*self.r) + self.r
    speed = random.random()*MAXSPEED
    angle = random.random()*2*PI
    self.vx = speed*math.cos(angle)
    self.vy = speed*math.sin(angle)

    self.ax=0
    self.ay=0

  def update_position(self):      
    self.x += self.vx
    self.y += self.vy
    self.vx += self.ax
    self.vy += self.ay

    if self.x < self.r or self.x > WIDTH-self.r or self.y < self.r or self.y > HEIGHT-self.r:
      self.reset()

    if random.random()<PROBAB_COLOR_CHANGE:
      self.color[0] = clamp(self.color[0] + random.random()*COLOR_CHANGE_MAXSTEP - COLOR_CHANGE_MAXSTEP/2, 0,255)
      self.color[1] = clamp(self.color[1] + random.random()*COLOR_CHANGE_MAXSTEP - COLOR_CHANGE_MAXSTEP/2, 0,255)
      self.color[2] = clamp(self.color[2] + random.random()*COLOR_CHANGE_MAXSTEP - COLOR_CHANGE_MAXSTEP/2, 0,255)    

LD = LaserDisplay()

shapes = []
for _ in range (NUM_SHAPES):
  particles = []
  for _ in range(NUM_POINTS):
    p = Particle(LD)
    particles.append(p)
    
  shapes.append(particles)

LD.set_noise(NOISE)
  
while True:
  LD.start_frame()
  for particles in shapes:
    points = []
    for p in particles:
      p.update_position()
      points.append([p.x,p.y])
      LD.set_color(p.color)
    LD.schedule(LD.quadratic_bezier_message(points, 10))
  LD.end_frame()

