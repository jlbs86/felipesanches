#!/usr/bin/env python
import sys
from popen2 import popen2
#from subprocess import Popen, PIPE

def to_hex(value):
	if value==0:
		return "0"

	result=""
	hex_algarism = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
	while value>0:
		result=hex_algarism[value%16]+result
		value/=16
	return result

def is_valid_opcode(arch, filename, address): 
	objdump_params = "-m %s -b binary -D %s --start-address=0x%s --stop-address=0x%s" % (arch, filename, to_hex(address), to_hex(address+20))

	(stdout, stdin) = popen2("objdump " + objdump_params + "| grep "+to_hex(address)+":")

#	p1 = Popen("objdump -D /home/felipe/devel/felipesanches/assembly/teste -b binary -m i386", stdout=PIPE)
#	p2 = Popen(["grep", to_hex(address)+":"], stdin=p1.stdout, stdout=PIPE)
#	output = p1.communicate()[0]

	line = stdout.readline()
	if "unknown" in line or "(bad)" in line:
		return False
	else:
		return True

def next_address(arch, filename, address): 
	objdump_params = "-m %s -b binary -D %s --start-address=0x%s --stop-address=0x%s" % (arch, filename, to_hex(address), to_hex(address+20))

	(stdout, stdin) = popen2("objdump " + objdump_params + "| grep "+to_hex(address)+":")

	line = stdout.readline()
	try:
		bytes = line.split("\t")[1]
	except:
		return -1
	bytes = "".join(bytes.split(" "))
	return address + len(bytes)

for arch in ["sparc", "i386", "powerpc", "m68k","alpha", "mips"]:
#	print arch + ": " + str(is_valid_opcode(arch, "teste", 513))
#	print "next: " + str(next_address(arch, "teste", 513))

	initial_address = int(sys.argv[1])
	current_address = initial_address
	filename = "teste"
	while(is_valid_opcode(arch, filename, current_address)):
		next = next_address(arch, filename, current_address)
		if next==-1 or next==current_address:
			break
		current_address = next

	print arch+": " + str(current_address-initial_address)
