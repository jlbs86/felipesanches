#!/usr/bin/env python

import time
from numpy import *
import math
from random import random

class LaserDevice():
  # Configuration flags
  ALWAYS_ON = 1
  SOMETHING = 2
  def __init__(self):
    self.messageBuffer = []
    self.ctm = matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
    self.flags = self.ALWAYS_ON

    import usb
    import time
    self.ReplayInitLog()
    time.sleep(3)

    # find our device
    self.usbdev = usb.core.find(idVendor=0x9999, idProduct=0x5555)

    # was it found?
    if self.usbdev is None:
        raise ValueError('Device (9999:5555) not found')

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    self.usbdev.set_configuration()

    # get an endpoint instance
    self.ep = usb.util.find_descriptor(
            self.usbdev.get_interface_altsetting(),   # first interface
            # match the first OUT endpoint
            custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT
        )

    assert self.ep is not None    

  def ReplayInitLog(self):
    import usb
   # find our device
    self.usbdev=None
    for bus in usb.busses():
      for dev in bus.devices:
        if dev.idVendor == 0x3333:
          self.usbdev = dev
    
    # was it found?
    if self.usbdev is None:
        raise ValueError('Device (3333:5555) not found')

    handle = self.usbdev.open() 
  
    print "Initializing device using data collected with USBSnoop"
    snifferlog = open("usbinit.log")

    for line in snifferlog.readlines():
      setup_packet = line.split("|")[0]
      buf = line.split("|")[-1]
      if len(buf):
        values = setup_packet.strip().split(" ")
        reqType = int(values[0],16)
        req = int(values[1],16)
 
        value = int(values[3],16)*256+int(values[2],16)
        index = int(values[5],16)*256+int(values[4],16)
        length = int(values[7],16)*256+int(values[6],16)

        value = int(values[2],16)*256+int(values[3],16)
        index = int(values[4],16)*256+int(values[5],16)
        length = int(values[6],16)*256+int(values[7],16)
 
        print "=== sending ==="
        print "bmRequestType: "+hex(reqType)
        print "bRequest: "+hex(req)
        print "wValue: "+hex(value)
        print "wIndex: "+hex(index)
        print "buffer: "+buf

        buf2 = ""
        for byte in buf.strip().split(" "):
          buf2+=chr(int(byte,16))

        handle.controlMsg(reqType,req,buf2,value,index)

    print "done."

  def set_flags(self, flags):
    self.flags = flags

#routines that generate USB messages (content of URBs):

  def line_message(self, x1,y1,x2,y2):
    x1+=random()*self.MaxNoise-self.MaxNoise/2
    y1+=random()*self.MaxNoise-self.MaxNoise/2
    x2+=random()*self.MaxNoise-self.MaxNoise/2
    y2+=random()*self.MaxNoise-self.MaxNoise/2
    
    x1,y1 = self.apply_context_transforms(x1,y1)
    x2,y2 = self.apply_context_transforms(x2,y2)

    x1 = clamp(x1,0,255)
    y1 = clamp(y1,0,255)
    x2 = clamp(x2,0,255)
    y2 = clamp(y2,0,255)
    
    return [x1, 0x00, y1, 0x00, self.color["R"], self.color["G"], self.color["B"], 0x03, x2, 0x00, y2, 0x00, self.color["R"], self.color["G"], self.color["B"], 0x02]

  def point_message(self, x, y):
    x+=random()*self.MaxNoise-self.MaxNoise/2
    y+=random()*self.MaxNoise-self.MaxNoise/2
    
    x,y = self.apply_context_transforms(x,y)
    x = clamp(x,0,255)
    y = clamp(y,0,255)

    return [x, 0x00, y, 0x00, self.color["R"], self.color["G"], self.color["B"], self.flags]
    
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
        if s == steps - 1 and i >= len(points) - 2:
          self.set_flags(0x02)
        message += (self.point_message(t_1 * (t_1 * points[i]  [0] + t * points[i+1][0]) + \
                                       t   * (t_1 * points[i+1][0] + t * points[i+2][0]),  \
                                       t_1 * (t_1 * points[i]  [1] + t * points[i+1][1]) + \
                                       t   * (t_1 * points[i+1][1] + t * points[i+2][1])))

    return message

  def cubic_bezier_message(self, points, steps):
    if len(points) < 4:
      print "Cubic Bezier curves have to have at least four points"
      return

    step_inc = 1.0/(steps)

    self.set_flags(0x03)
    message = self.point_message(points[0][0], points[0][1])
    self.set_flags(0x00)

    for i in range(0, len(points) - 3, 2):
      t = 0.0
      t_1 = 1.0
      for s in range(steps):
        t += step_inc
        t_1 = 1.0 - t
        if s == steps - 1 and i >= len(points) - 3:
          self.set_flags(0x02)
        message += self.point_message(t_1* (t_1 * (t_1 * points[i]  [0] + t * points[i+1][0]) + \
                                             t   * (t_1 * points[i+1][0] + t * points[i+2][0])) +
                                       t * (t_1 * (t_1 * points[i+1]  [0] + t * points[i+2][0]) + \
                                            t   * (t_1 * points[i+2][0] + t * points[i+3][0])),  \
                                       t_1 * (t_1 * (t_1 * points[i]  [1] + t * points[i+1][1]) + \
                                              t   * (t_1 * points[i+1][1] + t * points[i+2][1])) +
                                       t * (t_1 * (t_1 * points[i+1]  [1] + t * points[i+2][1]) + \
                                              t   * (t_1 * points[i+2][1] + t * points[i+3][1])))
    return message

#---------------

  def set_laser_configuration(self, blanking_delay, scan_rate):
    self.ep.write([blanking_delay, (45000 - scan_rate)/200])

  def set_color(self, c):
    self.color = {"R": c[0], "G": c[1], "B": c[2]}

  def draw_line(self, x1,y1,x2,y2):    
    self.schedule(self.line_message(x1, y1, x2, y2))

  def draw_quadratic_bezier(self, points, steps):
    message = self.quadratic_bezier_message(points, steps)
    if message:
      self.schedule(message)

  def draw_cubic_bezier(self, points, steps):
    message = self.cubic_bezier_message(points, steps)
    if message:
      self.schedule(message)

  def show_frame(self):
    self.ep.write(self.messageBuffer, 0)
    self.messageBuffer = []

  def schedule(self, message):
    self.messageBuffer += message

# routines that deal with coordinate system transforms:

  def apply_context_transforms(self, x,y):
    vector = self.ctm*matrix([x,y,1]).transpose()
    return vector[0], vector[1]

  def save(self):
    self.saved_matrix = self.ctm

  def restore(self):
    self.ctm = self.saved_matrix
    
  def rotate(self, angle):
    self.ctm = matrix([[math.cos(angle), -math.sin(angle), 0.0], [math.sin(angle), math.cos(angle), 0.0], [0.0, 0.0, 1.0]])*self.ctm

  def translate(self, x, y):
    self.ctm = matrix([[1.0, 0.0, float(x)], [0.0, 1.0, float(y)], [0.0, 0.0, 1.0]])*self.ctm
  
  def scale(self, s):
    self.ctm = matrix([[float(s), 0.0, 0.0], [0.0, float(s), 0.0], [0.0, 0.0, 1.0]])*self.ctm

  def rotate_at(self,cx,cy,angle):
    self.translate(-cx,-cy)
    self.rotate(angle)
    self.translate(cx,cy)
