#!/usr/bin/env python
# This example draws a dashed 2 color circle with increasing radius length
from LaserDisplay import LaserDisplay
import math
import pygame
import random

x=0x80
y=0x80
r=0x00
RED = [0x1F,0x80,0x00] #red
GREEN = [0x00,0xFF,0x00] #green
BLUE = [0x00,0x00,0xFF] #blue

CIRCLE = [[0.0,0.5],[0.0,1.0],[0.5,1.0],[1.0,1.0],[1.0,0.5],[1.0,0.0],[0.5,0.0],[0.0,0.0],[0.0,0.5]]
NUMBERS = [[[191, 130], [194, 194], [127, 191], [65, 191], [62, 129], [64, 62], [125, 62], [195, 65], [192, 131]], [[178, 133], [130, 149], [119, 191], [118, 116], [121, 62]], [[187, 131], [192, 189], [125, 192], [66, 190], [64, 149], [95, 97], [191, 66], [122, 63], [62, 64]], [[189, 161], [192, 197], [120, 193], [12, 188], [111, 126], [21, 64], [120, 60], [189, 64], [189, 96]], [[66, 127], [121, 128], [193, 125], [134, 156], [124, 194], [123, 128], [122, 64]], [[65, 192], [122, 192], [192, 192], [192, 161], [190, 133], [64, 137], [63, 99], [65, 63], [192, 64]], [[62, 160], [62, 193], [119, 194], [192, 194], [193, 133], [193, 65], [127, 62], [63, 64], [62, 99], [63, 130], [120, 131], [186, 125], [183, 93]], [[194, 191], [124, 191], [64, 191], [146, 142], [188, 63]], [[192, 164], [192, 193], [126, 195], [67, 192], [64, 165], [65, 137], [119, 133], [190, 134], [193, 102], [195, 64], [122, 60], [62, 64], [60, 89], [58, 119], [121, 132], [189, 134], [192, 166]], [[65, 191], [191, 193], [193, 159], [190, 115], [131, 120], [75, 144], [62, 190], [64, 123], [66, 63]]]

def gen_char(num, x, y, rx, ry):
  number = []
  for i in range(len(NUMBERS[num])):
    number.append([(int)(x + (NUMBERS[num][i][0])*rx),(int)(y + (NUMBERS[num][i][1])*ry)]);
  return number

def gen_circle(x, y, r):
  points = []
  for i in range(9):
    points.append([(int)(x + (CIRCLE[i][0]-0.5)*r*2), (int)(y + (CIRCLE[i][1]-0.5)*r*2-0.5)])
  return points

def draw_text(string, x, y, size, kerning_percentage = -0.3):
  char_pos = x
  for char in string:
    char_curve = gen_char(ord(char)-ord('0'), char_pos, y, size, size*2)
    LD.draw_bezier(char_curve, 5)
    char_pos -= int(size + size * kerning_percentage)

def draw_number(num, x, y, size, kerning_percentage = -0.3):
  draw_text(str(num), x, y, size, kerning_percentage)

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
BALL_RADIUS = 5
BAT_ACC = 1
BAT_MAXSPEED = 5
BALL_SPEED = 6

player1 = 128
player2 = 128
dir1 = 0
dir2 = 0
ballx = 128
bally = 128
ball_dx = BALL_SPEED
ball_dy = 0
acc1 = 0
acc2 = 0

time = 0
shutdown = 0
score1 = 0
score2 = 0

DIR_TBL = [8, 5, 2, 0, -2, -5, -8]
bounce_idx = 3

def clamp_int(value, min, max):
  if value > max: return max
  if value < min: return min
  return value

def reset():
  global player1, player2, dir1, dir2, ballx, bally, ball_dx, ball_dy, acc1, acc2
  player1 = 128
  player2 = 128
  dir1 = 0
  dir2 = 0
  ballx = 128
  bally = 128
  if random.random() > 0.5:
    ball_dx = BALL_SPEED
  else:
    ball_dx = -BALL_SPEED
  ball_dy = 0
  bounce_idx = int(random.random()*7)
  acc1 = 0
  acc2 = 0

def adjust_numbers():
  global NUMBERS
  LIST = []
  for N in NUMBERS:
    LIST.append(map(lambda(p):([p[0]/255.0,p[1]/255.0]),N))
  NUMBERS = LIST

adjust_numbers()

while shutdown != 1:
  clock.tick(FPS)
  time += 1

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        acc2 = BAT_ACC
      if event.key == pygame.K_a:
        acc2 = -BAT_ACC
      if event.key == pygame.K_o:
        acc1 = BAT_ACC
      if event.key == pygame.K_l:
        acc1 = -BAT_ACC
      if event.key == pygame.K_ESCAPE:
        shutdown = 1
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_q:
        acc2 -= BAT_ACC
        clamp_int(acc2, 0, BAT_ACC)
      if event.key == pygame.K_a:
        acc2 += BAT_ACC
        clamp_int(acc2, -BAT_ACC, 0)
      if event.key == pygame.K_o:
        acc1 -= BAT_ACC
        clamp_int(acc1, 0, BAT_ACC)
      if event.key == pygame.K_l:
        acc1 += BAT_ACC
        clamp_int(acc1, -BAT_ACC, 0)

  dir1 += acc1
  dir2 += acc2
  dir1 = clamp_int(dir1, -BAT_MAXSPEED, BAT_MAXSPEED)
  dir2 = clamp_int(dir2, -BAT_MAXSPEED, BAT_MAXSPEED)

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

  if ballx < PLAYER1_X + BALL_RADIUS:
    diff = bally - player1
    if diff > 20 or diff < -20:
      reset()
      score2 += 1
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
  if ballx > PLAYER2_X - BALL_RADIUS:
    diff = bally - player2
    if diff > 20 or diff < -20:
      reset()
      score1 += 1
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

  circle = gen_circle(ballx, bally, BALL_RADIUS)
  circle2 = gen_circle(ballx, bally, BALL_RADIUS-2)

  LD.set_color(RED)
  LD.draw_bezier(circle, 10)
  LD.set_color(GREEN)
  LD.draw_bezier(circle2, 6)
  LD.set_color([0xff,0x00,0x20])
  LD.draw_line(PLAYER1_X, player1-20, PLAYER1_X, player1+20)
  LD.set_color([0x20,0xff,0xff])
  LD.draw_line(PLAYER2_X, player2-20, PLAYER2_X, player2+20)

  draw_text("%02i"%(score1), 20, 220, 20)
  draw_text("%02i"%(score2), 235, 220, 20)
