all: 
	asx8051 -los dabusb_fw.d52 2> errors
	aslink -f dabusb_fw.lnk
	perl ezusb_convert.pl freefw < dabusb_fw.ihx > dabusb_fw.ihx.c

clean:
	rm -f *.ihx *.ihx.c *.map *.mem *.rel *.sym *.rst *.lst errors

