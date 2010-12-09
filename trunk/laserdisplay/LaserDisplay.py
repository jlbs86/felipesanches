#!/usr/bin/env python

import usb.core
import usb.util

class LaserDevice():
  def __init__(self):
    # find our device
    self.usbdev = usb.core.find(idVendor=0x9999, idProduct=0x5555)

    # was it found?
    if self.usbdev is None:
        raise ValueError('Device not found')

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    self.usbdev.set_configuration()

    # get an endpoint instance
    self.ep = self.usbusb.util.find_descriptor(
            self.usbdev.get_interface_altsetting(),   # first interface
            # match the first OUT endpoint
            custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT
        )

    assert self.ep is not None

    ALWAYS_ON = 1
    SOMETHING = 2

    self.FLAGS = 1

    CONFIG1 = 0
    CONFIG2 = 0

    self.color.R = 0x0
    self.color.G = 0
    self.color.B = 0xff

  def set_color(r,g,b):
    self.color.R = r
    self.color.G = g
    self.color.B = b
  
def line_message(x1,y1,x2,y2):
  return [x1, 0x00, y1, 0x00, self.color.R, self.color.G, self.color.B, self.flags, x2, 0x00, y2, 0x00, self.color.R, self.color.G, self.color.B, self.flags]

# write the data

x1 = 0
y1 = 0
x2=0xff
y2=0xff
x3=0x80
y3=0xff


PI=3.1415
import math

def draw_circle(x,y,r):
  global CONFIG
  set_color(0, 0xff, 0)
  step = 32
  for alpha in range(step):
    if alpha%2:
      set_color(0xff, 0, 0)
    else:
      set_color(0, 0, 0xff)

    CONFIG1=0
    CONFIG2=0
    if alpha==0:
      CONFIG1 = 3
    if alpha==step-1:
      CONFIG2 = 2
      
    ep.write(line_message(x + r*math.cos(alpha*2*PI/step), y + r*math.sin(alpha*2*PI/step), x + r*math.cos((alpha+1)*2*PI/step), y + r*math.sin((alpha+1)*2*PI/step)))

x=0x80
y=0x80
r=0x0


message = []
def start_frame():
  global message
  message = []

def end_frame():
  global message
  ep.write(message)

def add_line(x1,y1,x2,y2):
  global message
  for byte in line_message(x1, y1, x2, y2):
    message.append(byte)

def draw_line(x1,y1,x2,y2):
  ep.write(line_message(x1, y1, x2, y2))

while False:
  r+=1
  if r>0x30:
    r=0
  draw_circle(x, y, r)


while False:
  x1+=2
  y2+=1

  if x1>0xff:
    x1=0
  
  if y2>0xff:
    y2=0x0

  
  ep.write(line_message(x1, y1, x2, y2))
  ep.write(line_message(x2, y2, x3, y3))

