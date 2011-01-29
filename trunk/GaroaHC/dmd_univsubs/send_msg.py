#!/usr/bin/python
import serial
ser = serial.Serial(port="/dev/ttyUSB0")

ser.setBaudrate(19200)

msg1 = ""
msg2 = ""

while 42:
	ser.write("M")
	ser.write("%28s" % msg1.upper().strip())
	ser.write("%28s" % msg2.upper().strip())
	msg = raw_input("> ")
	msg1 = msg2
	msg2 = msg

ser.close()			# fecha a porta



