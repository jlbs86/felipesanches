#!/usr/bin/env python
#
# Youcope Emulator (adapted to render on a laser show display)
#
#(c)2010,2007 Felipe Sanches <juca@members.fsf.org>
#(c)2007 Leandro Lameiro <lameiro@gmail.com>
#licensed under GNU GPL v3 or later

import wave
import struct
import pygame
import sys
import math
from LaserDisplay import *

SIZE = (1.5*640,1.5*480)
DOTCOLOR  = (0,255,0)
GRIDCOLOR  = (40,40,0)
BGCOLOR = (0,0,0) #branco
FPS = 24
PERSISTENCE = 0.60

wro = wave.open('youscope-wave.wav')
READ_LENGTH = wro.getframerate()/FPS

pygame.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('YouScope XY-Demo Osciloscope Emulator')
pygame.mouse.set_visible(0)

clock = pygame.time.Clock()

grid = pygame.Surface(SIZE)
grid = grid.convert_alpha()
grid.set_alpha(128)
grid.fill(BGCOLOR)

for x in range(10):
    pygame.draw.line(grid, GRIDCOLOR, (x*SIZE[0]/10,0), (x*SIZE[0]/10,SIZE[0]))

for y in range(8):
    pygame.draw.line(grid, GRIDCOLOR, (0 , y*SIZE[1]/8), (SIZE[0] , y*SIZE[1]/8))

pygame.draw.line(grid, GRIDCOLOR, (SIZE[0]/2,0), (SIZE[0]/2,SIZE[0]), 3)
pygame.draw.line(grid, GRIDCOLOR, (0 , SIZE[1]/2), (SIZE[0] , SIZE[1]/2), 3)

for x in range(100):
    pygame.draw.line(grid, GRIDCOLOR, (x*SIZE[0]/100,SIZE[1]/2-3), (x*SIZE[0]/100,SIZE[1]/2+3))

for y in range(80):
    pygame.draw.line(grid, GRIDCOLOR, (SIZE[0]/2 - 3, y*SIZE[1]/80), (SIZE[0]/2 + 3, y*SIZE[1]/80))

surface = pygame.Surface(screen.get_size())

x_old=0
y_old=0

for _ in range(1000):
   frames = wro.readframes(READ_LENGTH)

display = LaserDisplay()
display.set_scan_rate(45000)
display.set_blanking_delay(0)
display.set_color(WHITE)

while True:
  try:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

#    for _ in range(30):
#      frames = wro.readframes(READ_LENGTH)
    
    frames = wro.readframes(READ_LENGTH)
    
    surface.fill(BGCOLOR)
    surface.blit(grid, grid.get_rect())
    SKIP=1
    for i in range(0,READ_LENGTH,4*SKIP):
      r = struct.unpack('hh', frames[i:i+4])
      x = int(r[1]*SIZE[0]/65536) + SIZE[0]/2 
      y = int(-r[0]*SIZE[1]/65536) + SIZE[1]/2
      surface.set_at((x,y), DOTCOLOR)
      #display.draw_line(x_old*256/SIZE[0],255-y_old*256/SIZE[1],x*256/SIZE[0],255-y*256/SIZE[1])
      display.draw_point(x*256/SIZE[0],255-y*256/SIZE[1])
      x_old=x
      y_old=y
      i+=4

#    display.show_frame()
    screen.blit(surface, surface.get_rect())
        
    pygame.display.flip()
    
  except:  
    #this is an ugly hack!
    display.show_frame()

