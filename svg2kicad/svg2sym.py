import sys
filename = sys.argv[1]

f = open(filename.split(".")[0] + ".sym", "w")

f.write('''EESchema-LIBRARY Version 2.3  SYMBOL  Date: Sex 18 Mai 2012 19:48:25 BRT
# SYMBOL TESTE
#
DEF TESTE BLAH 0 40 Y Y 1 0 N
DRAW
''')

r=0
g=1
b=0

class LDCLASS(object):
  points = []
  def draw_line(self, x1, y1, x2, y2):
    if (self.points==[]):
      self.points.append([x1, y1])

    if (self.points[-1] == [x1, y1]):
      self.points.append([x2, y2])
    else:
      self.draw_pline()
      self.points = [[x1, y1], [x2, y2]]

  def draw_pline(self):
    if self.points==[]:
      pass

    coordinate_pairs = ""
    for point in self.points:
      coordinate_pairs += " %d %d" % (point[0], -point[1])

    f.write("P %d %d %d %d %s N\n" % (len(self.points), r, g, b, coordinate_pairs))

  def draw_cubic_bezier(self):
    pass

LD = LDCLASS()

from xml.sax import make_parser
from xml.sax.handler import ContentHandler 

class SVGHandler(ContentHandler):
  def startElement(self, name, attrs):
    if name=="path":
      tokens = attrs.get('d').split(" ")
      i=0
      x,y=0,0
      x0,y0=x,y
      
      while i<len(tokens):
        if tokens[i].lower() in ["m", "c", "l", "h", "v", "z"]:
          cmd = tokens[i]
          i+=1
        
        if cmd=="m":
          delta=tokens[i].split(",")
          x+=float(delta[0])
          y+=float(delta[1])
          x0,y0=x,y
          cmd="l"
        elif cmd=="M":
          delta=tokens[i].split(",")
          x=float(delta[0])
          y=float(delta[1])
          x0,y0=x,y
          cmd="l"
        elif cmd=="l":
          delta=tokens[i].split(",")
          LD.draw_line(x,y,x+float(delta[0]),y+float(delta[1]))
          x+=float(delta[0])
          y+=float(delta[1])
        elif cmd=="L":
          delta=tokens[i].split(",")
          LD.draw_line(x,y,float(delta[0]),float(delta[1]))
          x=float(delta[0])
          y=float(delta[1])
        elif cmd=="z" or cmd=="Z":
          i-=1
          LD.draw_line(x,y,x0,y0)
          x,y=x0,y0
        elif cmd=="h":
          delta=tokens[i]
          LD.draw_line(x,y,x+float(delta),y)
          x+=delta
        elif cmd=="H":
          delta=tokens[i]
          LD.draw_line(x,y,float(delta),y)
          x=delta
        elif cmd=="v":
          delta=tokens[i]
          LD.draw_line(x,y,x,y+float(delta))
          y+=delta
        elif cmd=="V":
          delta=tokens[i]
          LD.draw_line(x,y,x,float(delta))
          y=delta
        elif cmd=="c":
          ctrl1=tokens[i].split(",")
          ctrl2=tokens[i+1].split(",")
          delta=tokens[i+2].split(",")
          LD.draw_cubic_bezier([[x,y],[x+float(ctrl1[0]),y+float(ctrl1[1])],[x+float(ctrl2[0]),y+float(ctrl2[1])],[x+float(delta[0]),y+float(delta[1])]],15)
          x+=float(delta[0])
          y+=float(delta[1])
          i+=2
        elif cmd=="C":
          ctrl1=tokens[i].split(",")
          ctrl2=tokens[i+1].split(",")
          delta=tokens[i+2].split(",")
          LD.draw_cubic_bezier([[x,y],[float(ctrl1[0]),float(ctrl1[1])],[float(ctrl2[0]),float(ctrl2[1])],[float(delta[0]),float(delta[1])]],15)
          x+=float(delta[0])
          y+=float(delta[1])
          i+=2
        i+=1

#we want to parse this: <path d=""/>
parser = make_parser()   
parser.setContentHandler(SVGHandler())
parser.parse(open(filename))

LD.draw_pline()

f.write('''ENDDRAW
ENDDEF
''')

f.close()

