#!/usr/bin/env python
import pygame

RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)

WIDTH  = 255
HEIGHT = 255

DISP_WIDTH  = 512
DISP_HEIGHT = 512

LINE_WIDTH = 3

MAX_LIFE = 200

SCALE_X = float(DISP_WIDTH)/WIDTH
SCALE_Y = float(DISP_HEIGHT)/HEIGHT

class Line():
  def __init__(self, p1, p2, color):
    self.p1 = p1
    self.p2 = p2
    self.color = color
    self.cur_color = color
    self.life = 0

  def update(self, millis):
    self.life += millis
    factor = 1.0 - self.life / float(MAX_LIFE)
    if (factor < 0.0):
      factor = 0.0
    self.cur_color = (int(self.color[0] * factor), int(self.color[1] * factor), int(self.color[2] * factor))

  def draw(self, surface):
    pygame.draw.line(surface, self.cur_color, self.p1, self.p2, LINE_WIDTH)

# Simulates what the observer would see on a white wall at night
class Wall():
  def __init__(self):
    self.linelist = []

  def update(self, millis):
    for line in self.linelist:
      line.update(millis)
    cut = 0
    for line in self.linelist:
      if line.life >= MAX_LIFE:
        cut += 1
      else:
        break
    self.linelist = self.linelist[cut:]

  def add_line(self, p1, p2, color):
    # Coordinate transformation
    p1 = (DISP_WIDTH - SCALE_X*p1[0], DISP_HEIGHT - SCALE_Y*p1[1])
    p2 = (DISP_WIDTH - SCALE_X*p2[0], DISP_HEIGHT - SCALE_Y*p2[1])

    self.linelist.append(Line(p1, p2, color))

  def draw(self, surface):
    surface.fill(BLACK)
    for line in self.linelist:
      line.draw(surface)

def clamp(value, min, max):
  if value > max: return max
  if value < min: return min
  return int(value)

class LasersimDevice():
  def __init__(self, config=None):
    pygame.init()

    self.surface = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
    self.lastpoint = (0,0)
    self.color = RED
    self.draw = False

    self.wall = Wall()

    self.messageBuffer = []

  def set_color(self, col):
    self.color = col

  def write(self, message):
    if len(message) == 0:
      return
    # For now, ignore configuration messages
    if len(message) < 8:
      return
    for i in range(0,len(message),8):
      newpoint = (message[i+0], message[i+2])
      if self.draw:
        self.wall.add_line(self.lastpoint, newpoint, self.color)
      self.lastpoint = newpoint
      self.color = (message[i+4], message[i+5], message[i+6])
      if message[i+7] == 0x03:
        self.draw = True
      if message[i+7] == 0x02:
        self.draw = False

  def set_flags(self, flags):
    self.flags = flags

  def point_message(self, x, y):
    x = clamp(x,0,255)
    y = clamp(y,0,255)

    return [x, 0x00, y, 0x00, self.color[0], self.color[1], self.color[2], self.flags]
    
  def quadratic_bezier_message(self, points, steps):
    if len(points) < 3:
      print "Quadratic Bezier curves have to have at least three points"
      return

    step_inc = 1.0/(steps)

    message = []
    self.set_flags(0x03)
    message += self.point_message(points[0][0], points[0][1])
    self.set_flags(0x00)

    for i in range(0, len(points) - 2, 2):
      t = 0.0
      t_1 = 1.0
      for s in range(steps):
        t += step_inc
        t_1 = 1.0 - t
        if s == steps - 1 and i >= len(points) - 3:
          self.set_flags(0x02)
        message += (self.point_message(t_1 * (t_1 * points[i]  [0] + t * points[i+1][0]) + \
                                       t   * (t_1 * points[i+1][0] + t * points[i+2][0]),  \
                                       t_1 * (t_1 * points[i]  [1] + t * points[i+1][1]) + \
                                       t   * (t_1 * points[i+1][1] + t * points[i+2][1])))

    return message

  def draw_quadratic_bezier(self, points, steps):
    message = self.quadratic_bezier_message(points, steps)
    if message:
      self.schedule(message)

  def schedule(self, message):
    self.messageBuffer += message

  def show_frame(self):
    self.write(self.messageBuffer)
    self.messageBuffer = []
    self.wall.draw(self.surface)
    self.wall.update(50)
    pygame.display.flip()

