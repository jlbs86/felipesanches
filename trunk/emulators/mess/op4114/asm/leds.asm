pause:
MOV R1, 0FFh
outer_loop:
MOV R0, 0FFh
inner_loop:
NOP
NOP
NOP
NOP
NOP
DJNZ R0, inner_loop
DJNZ R1, outer_loop
RET

write_panel_data:
;TODO
RET

start:

LCALL write_panel_data
LCALL pause

LJMP start

