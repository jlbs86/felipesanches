#!/usr/bin/env python

import telnetlib
import time

class LaserClient():
  def __init__(self, config={}):
    if not "server" in config:
      config["server"] = server
    if not "port" in config:
      config["port"] = port
    print "remote laser server config:\n server:%s port:%d" % (config["server"], config["port"])
    self.remote = telnetlib.Telnet(config["server"], config["port"])

  def set_laser_configuration(self, blanking_delay, scan_rate):
    self.remote.write("config %d %d\n" % (blanking_delay, scan_rate))

  def set_color(self, c):
    self.remote.write("color %d %d %d\n" % (c[0], c[1], c[2]))

  def draw_line(self, x1,y1,x2,y2):
    self.remote.write("line %d %d %d %d\n" % (x1, y1, x2, y2))

  def draw_quadratic_bezier(self, points, steps):
    msg = "quadratic"
    for p in points:
      msg+=" %f %f" % (p[0], p[1])
    self.remote.write(msg+"\n")

  def draw_cubic_bezier(self, points, steps):
    msg = "cubic"
    for p in points:
      msg+=" %f %f" % (p[0], p[1])
    self.remote.write(msg+"\n")

  def show_frame(self):
    self.remote.write("show\n")
    time.sleep(1.0/24)

  def save(self):
    self.remote.write("save\n")

  def restore(self):
    self.remote.write("restore\n")

  def rotate(self, angle):
    self.remote.write("rotate %d\n" % (angle))
    
  def translate(self, x, y):
    self.remote.write("translate %d %d\n" % (x,y))
  
  def scale(self, s):
    self.remote.write("scale %d\n" % (s))

  def rotate_at(self,cx,cy,angle):
    self.remote.write("rotateat %d %d %d\n" % (cx, cy, angle))

