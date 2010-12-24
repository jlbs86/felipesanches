#!/usr/bin/python

import pygame
from LaserDisplay import LaserDisplay
from LaserClient import *

pygame.init()

WIDTH = 512
HEIGHT = 512

CIRCLE = [[0.0,0.5],[0.0,1.0],[0.5,1.0],[1.0,1.0],[1.0,0.5],[1.0,0.0],[0.5,0.0],[0.0,0.0],[0.0,0.5]]

def gen_circle(x, y, r):
  points = []
  for i in range(9):
    points.append([(int)(x + (CIRCLE[i][0]-0.5)*r*2), (int)(y + (CIRCLE[i][1]-0.5)*r*2-0.5)])
  return points

size=WIDTH,HEIGHT;screen=pygame.display.set_mode(size, 0);
clock = pygame.time.Clock()

FPS = 30
cont = 1

numbers = []

curve = []
vec = []
ctl_x = 0
ctl_y = 0
curvelen = 0

config_snap = 1
config_border = 1

LD = LaserClient({"server":"localhost","port": 50000})
#LD = LaserDisplay()

def clamp_int(value, min, max):
  if value > max: return max
  if value < min: return min
  return value

while cont == 1:
#  clock.tick(FPS)

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        cont = 0
      if event.key == pygame.K_r:
        curve = []
        curvelen = 0
      if event.key == pygame.K_a:
        numbers.append(curve)
        print numbers
      if event.key == pygame.K_b:
        config_border = 1 - config_border
    if event.type == pygame.MOUSEBUTTONDOWN:
      x = clamp_int(255-(float)(event.pos[0])/WIDTH*255, 3, 252)
      y = clamp_int(255-(float)(event.pos[1])/HEIGHT*255, 3, 252)
      if config_snap:
        x = int(x)
        y = int(y)
      if curvelen % 2 == 0 and curvelen > 0:
        # Setting the control point
        last_point = curve[-1]
        curve[-1] = [ctl_x, ctl_y]
        curve.append(last_point)
      else:
        curve.append( [ x, y ] )
      curvelen += 1

  m_x = (float)(pygame.mouse.get_pos()[0])/WIDTH
  m_x = 1.0 - m_x
  m_y = (float)(pygame.mouse.get_pos()[1])/HEIGHT
  m_y = 1.0 - m_y

  m_x = clamp_int(m_x * 255, 6, 249)
  m_y = clamp_int(m_y * 255, 6, 249)

  if config_border:
    MIN_BORDER = 64
    MAX_BORDER = 192

    LD.set_color([0xff, 0x00, 0xff])
    mouse = gen_circle(MIN_BORDER, MIN_BORDER, 1)
    LD.draw_quadratic_bezier(mouse, 2)
    mouse = gen_circle(MIN_BORDER, MAX_BORDER, 1)
    LD.draw_quadratic_bezier(mouse, 2)
    mouse = gen_circle(MAX_BORDER, MAX_BORDER, 1)
    LD.draw_quadratic_bezier(mouse, 2)
    mouse = gen_circle(MAX_BORDER, MIN_BORDER, 1)
    LD.draw_quadratic_bezier(mouse, 2)

  mouse = gen_circle(m_x, m_y, 3)
  LD.draw_quadratic_bezier(mouse, 2)

  LD.set_color([0xff, 0x00, 0x00])
  if curvelen >= 3:
    LD.draw_quadratic_bezier(curve, 8);

  if curvelen % 2 == 0 and curvelen > 0:
    vec = [m_x - curve[-1][0], m_y - curve[-1][1]]
    ctl_x = curve[-1][0]-vec[0]
    ctl_y = curve[-1][1]-vec[1]
    circle = gen_circle(ctl_x, ctl_y, 2)

    #circle = gen_circle(curve[curvelen-1][0], curve[curvelen-1][1], 2)
    LD.set_color([0x00,0xff,0xff])
    LD.draw_quadratic_bezier(circle,4)
    LD.draw_quadratic_bezier([curve[-2],[ctl_x,ctl_y],curve[-1]], 5)

  LD.show_frame();
