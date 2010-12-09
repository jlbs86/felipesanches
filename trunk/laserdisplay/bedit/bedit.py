import pygame
from LaserDisplay import LaserDisplay

pygame.init()

WIDTH = 512
HEIGHT = 512

CIRCLE = [[0.0,0.5],[0.0,1.0],[0.5,1.0],[1.0,1.0],[1.0,0.5],[1.0,0.0],[0.5,0.0],[0.0,0.0],[0.0,0.5]]

def gen_circle(x, y, r):
  points = []
  for i in range(9):
    points.append([(int)(x + (CIRCLE[i][0]-0.5)*r*2), (int)(y + (CIRCLE[i][1]-0.5)*r*2-0.5)])
  return points

size=WIDTH,HEIGHT;screen=pygame.display.set_mode(size);
clock = pygame.time.Clock()

FPS = 30
cont = 1

curve = []
curvelen = 0

LD = LaserDisplay()

while cont == 1:
  clock.tick(FPS)

  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        cont = 0
    if event.type == pygame.MOUSEBUTTONDOWN:
      curvelen += 1
      curve.append( [ 255-(float)(event.pos[0])/WIDTH*255, 255-(float)(event.pos[1])/HEIGHT*255 ] )

  m_x = (float)(pygame.mouse.get_pos()[0])/WIDTH
  m_x = 1.0 - m_x
  m_y = (float)(pygame.mouse.get_pos()[1])/HEIGHT
  m_y = 1.0 - m_y

  m_x *= 255
  m_y *= 255

  if m_x < 6:
    m_x = 6
  if m_x > 249:
    m_x = 249
  if m_y < 6:
    m_y = 6
  if m_y > 249:
    m_y = 249

  LD.set_color([0xff, 0x00, 0xff])

  mouse = gen_circle(m_x, m_y, 3)
  LD.draw_bezier(mouse, 5)

  LD.set_color([0xff, 0x00, 0x00])
  if curvelen >= 3:
    LD.draw_bezier(curve, 8);
