#!/usr/bin/env python
# This example draws a dashed 2 color circle with increasing radius length
from LaserDisplay import LaserDisplay
import math
import pygame

x=0x80
y=0x80
r=0x00
RED = [0x1F,0x80,0x00] #red
GREEN = [0x00,0xFF,0x00] #green
BLUE = [0x00,0x00,0xFF] #blue

CIRCLE = [[0.0,0.5],[0.0,1.0],[0.5,1.0],[1.0,1.0],[1.0,0.5],[1.0,0.0],[0.5,0.0],[0.0,0.0],[0.0,0.5]]

def gen_circle(x, y, r):
  points = []
  for i in range(9):
    points.append([(int)(x + (CIRCLE[i][0]-0.5)*r*2), (int)(y + (CIRCLE[i][1]-0.5)*r*2-0.5)])
  return points

LD = LaserDisplay()

circle1 = gen_circle(0x80, 0x80, 0x10);
circle2 = gen_circle(0x80, 0x80, 0x18);
circle3 = gen_circle(0x80, 0x80, 0x20);

time = 0

FPS = 30

pygame.init()

size=width,height=320,200;screen=pygame.display.set_mode(size);
clock = pygame.time.Clock()

player1 = 128
player2 = 128
dir1 = 0
dir2 = 0
ballx = 128
bally = 128

while True:
  clock.tick(FPS)
  time += 1

  acc1 = 0
  acc2 = 0

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        acc2 += 3
      if event.key == pygame.K_a:
        acc2 -= 3
      if event.key == pygame.K_o:
        acc1 += 3
      if event.key == pygame.K_l:
        acc1 -= 3
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_q:
        acc2 -= 3
      if event.key == pygame.K_a:
        acc2 += 3
      if event.key == pygame.K_o:
        acc1 -= 3
      if event.key == pygame.K_l:
        acc1 += 3

  dir1 += acc1
  dir2 += acc2

  player1 += dir1
  player2 += dir2

  if player1 < 20:
    player1 = 20
  if player1 > 230:
    player1 = 230
  if player2 < 20:
    player2 = 20
  if player2 > 230:
    player2 = 230

  x_coord = (int)(math.cos(time/200.0) * 40) + 128
  y_coord = (int)(math.sin(time/200.0) * 40) + 128

  circle = gen_circle(x_coord, y_coord, 5)
  circle2 = gen_circle(x_coord, y_coord, 3)

  LD.set_color(RED)
  LD.draw_bezier(circle, 10)
  LD.set_color(GREEN)
  LD.draw_bezier(circle2, 6)
  LD.set_color([0xff,0x00,0x20])
  LD.draw_line(20, player1-20, 20, player1+20)
  LD.set_color([0x20,0xff,0xff])
  LD.draw_line(230, player2-20, 230, player2+20)

