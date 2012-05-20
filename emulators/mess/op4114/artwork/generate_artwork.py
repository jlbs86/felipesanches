f = open("op4114.lay", "w")

f.write('''<?xml version="1.0"?>
<mamelayout version="2">
	<element name="LED" defstate="1">
		<rect>
			<color red="0.7" green="0.0" blue="0.0" />
		</rect>
	</element>

	<element name="BUTTON" defstate="0">
		<rect>
			<color red="0.8" green="0.8" blue="0.7" />
		</rect>
	</element>

	<element name="background">
		<image file="op4114.png" />
	</element>

	<view name="Default Layout">
		<!-- background -->
		<backdrop element="background">
			<bounds left="0" top="0" right="1024" bottom="768" />
		</backdrop>

''')

x0 = [603.768, 708.183, 833.962, 938.211]
xN = [608.466, 717.021, 849.599, 957.475]

y0 = 121.834
yN = 530.163

y_step = (yN-y0) / 15
led_w = 10
led_h = led_w

led=0
for coluna in range(4):
  x_step = (xN[coluna]-x0[coluna])/15
  for linha in range(16):
    left = x0[coluna] + linha*x_step
    right = left + led_w
    top = y0 + linha * y_step
    bottom = top + led_h

    f.write('''
		<bezel name="led%d" element="LED">
			<bounds left="%d" right="%d" top="%d" bottom="%d" />
		</bezel>
''' % (led, left, right, top, bottom))

    led+=1

f.write('''
	</view>
</mamelayout>
''')
f.close()
