.psp
.relativeinclude off

.open "BOOT.BIN.patched", 0x08803F60

.orga 0x761c
	.area 4
	; Home menu language:
	; 0 - ja
	; 1 - eng
	; 8 - ru
	li a0, 1
.endarea

.orga 0x7624
.area 4
	; Home button layout
	; 0 - O=OK; 1 - X=OK
	li a1, 0
.endarea

; Decrease line spacing in fullscreen text.
.org 0x881CCB0
.area 4
	addiu a2, v0, -0x1
.endarea

; Fix the text bug for "All Choices:". (Inlined strcpy)
.org 0x8828084
.area 4*3, 0
	lw    v0, 0x14(v1)
	blez  s1,0x08828498
	sw    v0, 0x14(s0)
.endarea


; Decrease spacing between characters in scene texts (originally 2 px)
; (Doesn't apply to menus, choice texts, history)
@FontSpacing equ 0x1
; .org 0x881AA9C - width calc subroutine address
.org 0x881AAF4
;	nop
	addiu v0, v0, @FontSpacing
.org 0x881AB20
;	nop
	addiu v0, v0, @FontSpacing
.org 0x881AB50
	addiu v0, v1, @FontSpacing


; Comparator with a string of unbreakable symbols. Rewrote it to only check the 1st ascii byte.
; returns v0: 1 - if matched, 0 - not matched
.org 0x881A984
.area 4*18, 0
	lb	a2, 0x0(a0)
	addiu a0, a2, -0x80
	bgez a0, @@NotMatched   ;don't even try to match jap symbols
	nop
	lb	v0, 0x0(a1)
.resetdelay
@@CheckNext:
	beq	v0,zero, @@NotMatched
	addiu a1, a1,1
	bnel v0,a2, @@CheckNext
	lb	v0, 0x0(a1)
@@Matched:
	jr	ra
	li	v0,0x1
@@NotMatched:
	jr	ra
	li	v0,0
.endarea


.close
