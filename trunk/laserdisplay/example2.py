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
NUMBERS = [
  [[0.0,0.5],[0.0,1.0],[0.5,1.0],[1.0,1.0],[1.0,0.5],[1.0,0.0],[0.5,0.0],[0.0,0.0],[0.0,0.5]],
  [[0.0,0.0],[0.0,0.5],[0.0,1.0]],
  [[0.0,0.5],[0.0,1.0],[0.9,1.0],[1.8,0.5],[0.0,0.0],[0.5,0.0],[1.0,0.0]]
]

def gen_number(num, x, y, rx, ry):
  number = []
  for i in range(len(NUMBERS[num])):
    number.append([(int)(x + (NUMBERS[num][i][0]-0.5)*rx),(int)(y + (NUMBERS[num][i][1]-0.5)*ry)]);
  return number

def gen_circle(x, y, r):
  points = []
  for i in range(9):
    points.append([(int)(x + (CIRCLE[i][0]-0.5)*r*2), (int)(y + (CIRCLE[i][1]-0.5)*r*2-0.5)])
  return points

LD = LaserDisplay()

circle1 = gen_circle(0x80, 0x80, 0x10);
circle2 = gen_circle(0x80, 0x80, 0x18);
circle3 = gen_circle(0x80, 0x80, 0x20);

pygame.init()

size=width,height=320,200;screen=pygame.display.set_mode(size);
clock = pygame.time.Clock()

FPS = 30
PLAYER1_X = 20
PLAYER2_X = 230
BARRIER1 = 15
BARRIER2 = 235
BARRIER_TOP = 235
BARRIER_BOTTOM = 15

player1 = 128
player2 = 128
dir1 = 0
dir2 = 0
ballx = 128
bally = 128
ball_dx = 2
ball_dy = 0
acc1 = 0
acc2 = 0

time = 0
shutdown = 0

DIR_TBL = [3, 2, 1, 0, -1, -2, -3]
bounce_idx = 3

def reset():
  global player1, player2, dir1, dir2, ballx, bally, ball_dx, ball_dy, acc1, acc2
  player1 = 128
  player2 = 128
  dir1 = 0
  dir2 = 0
  ballx = 128
  bally = 128
  ball_dx = 2
  ball_dy = 0
  bounce_idx = 3
  acc1 = 0
  acc2 = 0

while shutdown != 1:
  clock.tick(FPS)
  time += 1

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        acc2 += 2
      if event.key == pygame.K_a:
        acc2 -= 2
      if event.key == pygame.K_o:
        acc1 += 2
      if event.key == pygame.K_l:
        acc1 -= 2
      if event.key == pygame.K_ESCAPE:
        shutdown = 1
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_q:
        acc2 -= 2
      if event.key == pygame.K_a:
        acc2 += 2
      if event.key == pygame.K_o:
        acc1 -= 2
      if event.key == pygame.K_l:
        acc1 += 2

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

  ball_dy = DIR_TBL[bounce_idx]

  ballx += ball_dx
  bally += ball_dy

  region = -1

  if ballx < PLAYER1_X:
    diff = bally - player1
    if diff > 20 or diff < -20:
      reset()
    elif diff >= 15:
      region = 0
    elif diff >= 10:
      region = 1
    elif diff > -10:
      region = 2
    elif diff > -15:
      region = 3
    else:
      region = 4
  if ballx > PLAYER2_X:
    diff = bally - player2
    if diff > 20 or diff < -20:
      reset()
    elif diff >= 15:
      region = 0
    elif diff >= 10:
      region = 1
    elif diff > -10:
      region = 2
    elif diff > -15:
      region = 3
    else:
      region = 4

  if region != -1:
    bounce_idx = region + bounce_idx - 2
    if bounce_idx < 0: bounce_idx = 0
    if bounce_idx > 6: bounce_idx = 6
    ball_dx = -ball_dx

  if bally < BARRIER_BOTTOM or bally > BARRIER_TOP:
    bounce_idx = 6 - bounce_idx

  if (ballx < BARRIER1):
    reset()
  if (ballx > BARRIER2):
    reset()

  circle = gen_circle(ballx, bally, 5)
  circle2 = gen_circle(ballx, bally, 3)

  LD.set_color(RED)
  LD.draw_bezier(circle, 10)
  LD.set_color(GREEN)
  LD.draw_bezier(circle2, 6)
  LD.set_color([0xff,0x00,0x20])
  LD.draw_line(PLAYER1_X, player1-20, PLAYER1_X, player1+20)
  LD.set_color([0x20,0xff,0xff])
  LD.draw_line(PLAYER2_X, player2-20, PLAYER2_X, player2+20)

  number1 = gen_number(2, 128, 245, 8, 20)
  LD.set_color(RED)
  LD.draw_bezier(number1, 4)

