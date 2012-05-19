inicio:
	mov	r0,#0
	mov	dptr,#0000
main:
	push dph
	push dpl
	mov	r2,#4
loop:
	mov a, r0
	push dph
	push dpl
	mov dptr,#sprites
	movc a,@a+dptr
	pop dpl
	pop dph

	movx	@dptr,a
	inc	dptr
	inc	dptr
  inc r0
	djnz	r2, loop

  lcall pausa
	pop dpl
	pop dph

  cjne r0, #4, inicio
  ljmp main

pausa:
	mov r3, 0FFh 
pausa_loop_out:
	mov r4, 0FFh
pausa_loop_in:
  nop
  nop
  nop
  nop
  djnz r4, pausa_loop_in
  djnz r3, pausa_loop_out
  ret

sprites:
	.db 7Fh, 88h, 88h, 7Fh

; letra A
; 0 x - - x 
; 1 - x x -
; 2 - x x -
; 3 - x x -
; 4 - - - -
; 5 - x x -
; 6 - x x -
; 7 - x x -

	.db 0FFh, 91h, 91h, 06Eh ;letra B
; 0 - - - x
; 1 - x x -
; 2 - x x -
; 3 - - - x
; 4 - x x -
; 5 - x x -
; 6 - x x -
; 7 - - - x

; 0 x x x x
; 1 x x x x
; 2 x x x x
; 3 x x x x
; 4 x x x x
; 5 x x x x
; 6 x x x x
; 7 x x x x
