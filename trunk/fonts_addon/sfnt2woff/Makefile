all: lib_woff2sfnt.so

lib_woff2sfnt.so: lib_woff2sfnt.o woff.o
	ld woff.o lib_woff2sfnt.o --shared -o lib_woff2sfnt.so

lib_woff2sfnt.o: lib_woff2sfnt.c woff.h Makefile

woff.o: woff.c woff.h woff-private.h Makefile

clean:
	$(RM) -r *.o *.dSYM
