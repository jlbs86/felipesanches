#!/usr/bin/env python

num_nets=8
num_dots=300
max_width=1000000
max_height=1000000
filename="art.pcb"
via_diameter = 11000
spacing = via_diameter/4

report_collisions = True
max_percentage = 0.70

slots = int(max_width/via_diameter) * int(max_height/via_diameter)
if num_dots > slots*max_percentage:
  print 'too much dots! Max allowed is %d' % int(slots*max_percentage)
  exit()

#####################
def output_header(fp, max_width, max_height):
  fp.write(
'''
# release: pcb 20080202
# date:    Mon Apr 26 18:25:23 2010
# user:    felipe (felipe,,,)
# host:    simon

# To read pcb files, the pcb version (or the cvs source date) must be >= the file version
FileVersion[20070407]

PCB["" %d %d]

Grid[5000.000000 0 0 1]
Cursor[0 0 6.000000]
PolyArea[200000000.000000]
Thermal[0.500000]
DRC[1000 1000 1000 1000 1500 1000]
Flags("rubberband,nameonpcb,autodrc,orthomove")
Groups("1,2,3,s:4,5,6,c:s:c")
Styles["Signal,1000,4000,2000,1000:Power,2500,6000,3500,1000:Fat,4000,6000,3500,1000:Skinny,800,3600,2000,1000"]
''' % (max_width, max_height))


def output_dot(fp, dot_id, x,y):
  fp.write(
'''
Element["" "a_dot" "D%d" "" %d %d 7600 59000 1 150 ""]
(
	Pin[0 0 11000 3000 14000 4800 "1" "1" ""]
	)
''' % (dot_id, x, y))

def output_pair(fp, dot_id, x,y):
  fp.write(
'''
Element["" "a_pair" "P%d" "" %d %d 7600 59000 1 150 ""]
(
	Pin[0 0 11000 3000 14000 4800 "1" "1" ""]
	Pin[0 38800 11000 3000 14000 4800 "2" "2" ""]
	)
''' % (dot_id, x, y))

def output_layers(fp):
  fp.write(
'''
Layer(4 "component")
(
)
Layer(7 "silk")
(
)
''')

def output_netlist(fp, netlist):
  fp.write("\nNetList()\n(\n")

  for k in netlist.keys():
    fp.write('\tNet("net%d" "(unknown)")\n\t(\n' % (k))
    for el in netlist[k]:
      fp.write('\t\tConnect("D%d-1")\n' % (el))
    fp.write("\t)\n")
  fp.write(")\n")

import math
def hit(p, x,y):
  px,py = p
  d = math.sqrt((px-x)**2 + (py-y)**2)
  return d < via_diameter+spacing

points={}
def point_collision(x,y):
  global points
  x_key = int(x/via_diameter)
  y_key = int(y/via_diameter)
  key = x_key,y_key
  print x, y, key

  try:
    test = points[key]
  except KeyError:
    points[key]=[]

  for i in range(x_key-2,x_key+2):
    for j in range(y_key-2,y_key+2):
      try:
        for p in points[(i,j)]:
          if hit(p, x,y):
            if report_collisions:
              print "collision!"
            return True
      except KeyError:
        pass

  points[key].append((x,y))
  return False

#######################################
fp = open(filename, "w")
output_header(fp, max_width, max_height)
netlist = {}
for i in range(num_nets):
  netlist[i]=[]

from random import randint, random
def sort_square(w,h):
  x = randint(0, w-1)
  y = randint(0, h-1)
  return x,y

def sort_circle(xc,yc,radius):
  r = random() * radius
  alpha = random()*2*3.1415
  x = xc + r*math.cos(alpha)
  y = yc + r*math.sin(alpha)
  return x,y

def sort_circle_homogeneous(xc,yc,radius):
  x,y = sort_square(2*radius,2*radius)
  while radius < math.sqrt((x-xc)**2 + (y-yc)**2):
    x,y = sort_square(2*radius,2*radius)

  return x,y

for dot_id in range(num_dots):
  net = randint(0, num_nets-1)
  netlist[net].append(dot_id)


#    x,y = sort_square(max_width, max_height)
#    while point_collision(x,y):
#      x,y = sort_square(max_width, max_height)

  xc, yc = max_width/2, max_height/2
  if xc < yc:
    radius = xc
  else:
    radius = yc

#  x,y=sort_circle(xc, yc, radius)
#  while point_collision(x,y):
#    x,y=sort_circle(xc, yc, radius)

  x,y=sort_circle_homogeneous(xc, yc, radius)
  while point_collision(x,y):
    x,y=sort_circle_homogeneous(xc, yc, radius)

  output_dot(fp, dot_id, x, y)

output_layers(fp)
output_netlist(fp, netlist)
fp.close()

