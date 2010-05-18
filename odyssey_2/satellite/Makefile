all: rom run

rom: satellite.rom

run: satellite.rom
	o2em satellite.rom

satellite.rom: satellite.p
	p2bin $< $@ -r \$$400-\$$fff

%.p: %.a48
	asl -a -u -q -i .. $< -o $@

cos_table.inc: cos_table.py
	python cos_table.py >$@

%.i: %.pnm
	perl ppmtosprite.pl $< >$@

clean:
	rm -f satellite.p *.i *.inc

# dependencies
satellite.p: g7000.h satellite.i cos_table.inc

