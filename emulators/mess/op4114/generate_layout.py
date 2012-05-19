f = open("op4114.lay", "w")

f.write('''<?xml version="1.0"?>
<mamelayout version="2">
	<element name="LED" defstate="1">
		<rect>
			<color red="1.0" green="0.0" blue="0.0" />
		</rect>
	</element>

	<element name="LEDOFF">
		<rect>
			<color red="0.3" green="0.3" blue="0.3" />
		</rect>
	</element>

	<element name="BUTTON" defstate="0">
		<rect>
			<color red="0.8" green="0.8" blue="0.7" />
		</rect>
	</element>

	<element name="background">
		<rect>
			<color red="0.6" green="0.6" blue="0.6" />
		</rect>
	</element>

	<view name="Default Layout">
		<!-- background -->
		<backdrop element="background">
			<bounds left="0" top="0" right="453" bottom="235" />
		</backdrop>

''')

x0 = 260
y0 = 10
x_step = 56
y_step = x_step/4
button_w = 15
led_w = button_w/2
led_h = led_w

led=0
for coluna in range(4):
  for linha in range(16):

    left = x0 + coluna * x_step
    right = left + led_w
    top = y0 + linha * y_step
    bottom = top + led_h

    f.write('''
		<bezel name="ledoff%d" element="LEDOFF">
			<bounds left="%d" right="%d" top="%d" bottom="%d" />
		</bezel>
''' % (led, left, right, top, bottom))

    f.write('''
		<bezel name="led%d" element="LED">
			<bounds left="%d" right="%d" top="%d" bottom="%d" />
		</bezel>
''' % (led, left, right, top, bottom))

    left = left + led_w + 1
    right = left + button_w
    f.write('''
		<bezel name="button%d" element="BUTTON">
			<bounds left="%d" right="%d" top="%d" bottom="%d" />
		</bezel>
''' % (led, left, right, top, bottom))
    led+=1

f.write('''
	</view>
</mamelayout>
''')
f.close()
