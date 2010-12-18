import usb
import time
from numpy import *
from random import random


PI=3.1415926536
WIDTH=255
HEIGHT=255

RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
CYAN = [0,255,255]
MAGENTA = [255,0,255]
YELLOW = [255,255,0]
WHITE = [255,255,255]

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


def clamp(value, min, max):
  value = max - value
  if value > max: return max
  if value < min: return min
  return int(value)

class LaserDisplay:

  ALWAYS_ON = 1
  MaxNoise = 0
  messageBuffer = []
  ctm = matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
  flags = ALWAYS_ON
  usbdev = None
  blanking_delay = 202
  scan_rate = 37000

  def __init__(self):
    self.sendInitialization()

    self.usbdev = usb.core.find(idVendor=0x9999, idProduct=0x5555)

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

    self.adjust_glyphs()
    self.set_color(WHITE)
    self.set_laser_configuration(self.blanking_delay, self.scan_rate)



  def sendInitialization(self):
    usbdev = usb.core.find(idVendor=0x3333, idProduct=0x5555)
    if usbdev is None:
        print 'Device (3333:5555) not found, not initialising'
        return
    handle = usbdev.open()

    print 'Initializing device ...',
    snifferlog = open('usbinit.log')

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

        binbuf = ''
        for byte in buf.strip().split(" "):
          binbuf += chr(int(byte,16))

        handle.controlMsg(reqType,req,binbuf,value,index)

    print 'done'
    time.sleep(1)



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
      print 'Quadratic Bezier curves have to have at least three points'
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



  def set_laser_configuration(self, blanking_delay, scan_rate):
    self.ep.write([blanking_delay, (45000 - scan_rate)/200])



  def set_color(self, c):
    if len(c) == 3:
        self.color = {"R": c[0], "G": c[1], "B": c[2]}
    elif len(c) == 7:
        self.color = {"R": int(c[1:3],16), "G": int(c[3:5],16), "B": int(c[5:7],16)}



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


  def adjust_glyphs(self):
    for k in GLYPHS.keys():
      GLYPHS[k] = map(lambda(p):([p[0]/255.0,p[1]/255.0]),GLYPHS[k])



  def set_noise(self, value):
    self.MaxNoise = value



  def set_scan_rate(self, value):
    if value<5000:
      value = 5000
      print "minimum allowed scan rate value is 5000"
    if value>45000:
      value = 45000
      print "maximum allowed scan rate value is 45000"
    self.scan_rate = value
    self.set_laser_configuration(self.blanking_delay, self.scan_rate)



  def set_blanking_delay(self, value):
    if value<0:
      value = 0
      print "minimum allowed blanking delay value is 0"
    if value>255:
      value = 255
      print "maximum allowed blanking delay value is 255"
    self.blanking_delay = value
    self.set_laser_configuration(self.blanking_delay, self.scan_rate)



  def gen_glyph_data(self, char, x, y, rx, ry):
    glyph_data = []
    for i in range(len(GLYPHS[char])):
      glyph_data.append([(int)(x + (GLYPHS[char][i][0])*rx),(int)(y + (GLYPHS[char][i][1])*ry)]);
    return glyph_data



  def draw_text(self, string, x, y, size, kerning_percentage = -0.3):
    for char in string:
      glyph_curve = self.gen_glyph_data(char, x, y, size, size*2)
      self.draw_quadratic_bezier(glyph_curve, 5)
      x -= int(size + size * kerning_percentage)

  def draw_dashed_circle(self, x,y,r, c1, c2):
    step = 32
    for alpha in range(step):
      if alpha%2:
        self.set_color(c1)
      else:
        self.set_color(c2)
      self.draw_line(x + r*math.cos(alpha*2*PI/step), y + r*math.sin(alpha*2*PI/step), x + r*math.cos((alpha+1)*2*PI/step), y + r*math.sin((alpha+1)*2*PI/step))
