all: rom run

rom: satellite.rom

run: satellite.rom
	o2em satellite.rom

satellite.rom: satellite.p
	p2bin $< $@ -r \$$400-\$$fff

%.p: %.a48
	asl -a -u -q -i .. $< -o $@

%.i: %.pnm
	perl ppmtosprite.pl $< >$@

clean:
	rm -f satellite.p *.i

# dependencies
satellite.p: g7000.h satellite.i

