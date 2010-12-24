#!/usr/bin/env python

from LasersimDevice import LasersimDevice
from LaserDevice import LaserDevice
from types import *
import traceback
import sys

#TODO: Create a file with colors

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
CYAN = [0,255,255]
MAGENTA = [255,0,255]
YELLOW = [255,255,0]
WHITE = [255,255,255]

class LaserDisplay():
  # Shapes for our characher rendering routine
  GLYPHS = {"0": [[191, 130], [194, 194], [127, 191], [65, 191], [62, 129], [64, 62], [125, 62], [195, 65], [192, 131]],
  "1": [[178, 133], [130, 149], [119, 191], [118, 116], [121, 62]],
  "2": [[187, 131], [192, 189], [125, 192], [66, 190], [64, 149], [95, 97], [191, 66], [122, 63], [62, 64]],
  "3": [[189, 161], [192, 197], [120, 193], [12, 188], [111, 126], [21, 64], [120, 60], [189, 64], [189, 96]],
  "4": [[66, 127], [121, 128], [193, 125], [134, 156], [124, 194], [123, 128], [122, 64]],
  "5": [[65, 192], [122, 192], [192, 192], [192, 161], [190, 133], [64, 137], [63, 99], [65, 63], [192, 64]],
  "6": [[62, 160], [62, 193], [119, 194], [192, 194], [193, 133], [193, 65], [127, 62], [63, 64], [62, 99], [63, 130], [120, 131], [186, 125], [183, 93]],
  "7": [[194, 191], [124, 191], [64, 191], [146, 142], [188, 63]],
  "8": [[192, 164], [192, 193], [126, 195], [67, 192], [64, 165], [65, 137], [119, 133], [190, 134], [193, 102], [195, 64], [122, 60], [62, 64], [60, 89], [58, 119], [121, 132], [189, 134], [192, 166]],
  "9": [[65, 191], [191, 193], [193, 159], [190, 115], [131, 120], [75, 144], [62, 190], [64, 123], [66, 63]],
  ":": []}

  def __init__(self, config=None):
    if config and "simulator" in config:
      self.device = LasersimDevice(config)
    else:
      self.device = LaserDisplayLocalDevice()
   
    self.adjust_glyphs()

    #default values
    self.blanking_delay = 202
    self.scan_rate = 37000
    self.call("set_color", WHITE)
    self.MaxNoise = 0
    self.call("set_laser_configuration", self.blanking_delay, self.scan_rate)

  # Call proxymethod that calls the corresponding method in the underlaying device (if defined)
  def call(self, method_name, *args):
    try:
      method = eval("self.device."+method_name)
    except AttributeError as exc:
      print "STUB: Method", method_name, "not defined on class", self.device.__class__.__name__
      traceback.print_exc()
      return
    eval("self.device."+method_name+repr(args))

  def adjust_glyphs(self):
    for k in self.GLYPHS.keys():
      self.GLYPHS[k] = map(lambda(p):([p[0]/255.0,p[1]/255.0]),self.GLYPHS[k])

  def set_noise(self, value):
    self.MaxNoise = value

  def set_color(self, c):
    self.device.set_color(c)
      
  def set_scan_rate(self, value):
    if value<5000:
      value = 5000
      print "minimum allowed scan rate value is 5000"
    if value>45000:
      value = 45000
      print "maximum allowed scan rate value is 45000"
    self.scan_rate = value
    self.device.call("set_laser_configuration", self.blanking_delay, self.scan_rate)
    
  def set_blanking_delay(self, value):
    if value<0:
      value = 0
      print "minimum allowed blanking delay value is 0"
    if value>255:
      value = 255
      print "maximum allowed blanking delay value is 255"
    self.blanking_delay = value
    self.call("set_laser_configuration", self.blanking_delay, self.scan_rate)

  def set_laser_configuration(self, blanking_delay, scan_rate):
    self.blanking_delay = blanking_delay
    self.scan_rate = scan_rate
    self.call("set_laser_configuration", self.blanking_delay, self.scan_rate)

  def draw_point(self, x,y):
    self.call("draw_line",x,y,x,y)

  def draw_line(self, x1,y1,x2,y2):
    self.call("draw_line",x1,y1,x2,y2)

  def draw_quadratic_bezier(self, points, steps):
    self.call("draw_quadratic_bezier", points, steps)

  def draw_cubic_bezier(self, points, steps):
    self.call("draw_cubic_bezier", points, steps)

  def show_frame(self):
    self.call("show_frame")
    
  def save(self):
    self.call("save")

  def restore(self):
    self.call("restore")
    
  def rotate(self, angle):
    self.call("rotate", angle)

  def translate(self, x, y):
    self.call("translate", x, y)
  
  def scale(self, s):
    self.call("scale", s)

  def rotate_at(self,cx,cy,angle):
    self.call("rotate_at", cx,cy,angle)

  def gen_glyph_data(self, char, x, y, rx, ry):
    glyph_data = []
    for i in range(len(self.GLYPHS[char])):
      glyph_data.append([(int)(x + (self.GLYPHS[char][i][0])*rx),(int)(y + (self.GLYPHS[char][i][1])*ry)]);
    return glyph_data

  def draw_text(self, string, x, y, size, kerning_percentage = -0.3):
    for char in string:
      glyph_curve = self.gen_glyph_data(char, x, y, size, size*2)
      self.call("draw_quadratic_bezier", glyph_curve, 5)
      x -= int(size + size * kerning_percentage)

