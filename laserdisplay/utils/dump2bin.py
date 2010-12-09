input = open("dump.text").readline().strip()
output = open("dump.bin", "w")

mylist = [input[i:i+2] for i in range(0,len(input),2)]
for byte in mylist:
  output.write(chr(int(byte,16)))

