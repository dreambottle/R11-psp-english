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

; Fix the text bug for "All Choices:". (Inlined strcpy didn't copy the last char)
.org 0x8828084
.area 4*3, 0
	lw    v0, 0x14(v1)
	blez  s1,0x08828498
	sw    v0, 0x14(s0)
.endarea


; Decrease spacing between characters in scene texts (originally 2 px)
; (Doesn't apply to menus, choice texts, history)
@FontSpacing equ 0x0
; .org 0x881AA9C - width calc subroutine address
.org 0x881AAF4
;	nop
	addiu v0, v0, @FontSpacing
.org 0x881AB20
;	nop
	addiu v0, v0, @FontSpacing
.org 0x881AB50
	addiu v0, v1, @FontSpacing


; Comparator for a string of unbreakable symbols. Rewrote it to only check the 1st ascii byte.
; returns v0: 1 - if matched, 0 - not matched
.org 0x0881A984
.area 4*18, 0
	lbu	a2, 0x0(a0)
	lbu	v1, 0x0(a1)
@@CheckNext:
	beq	v1,zero, @@NotMatched
	addiu a1, a1,1
	bnel v1,a2, @@CheckNext
	lbu	v1, 0x0(a1)
@@Matched:
	jr	ra
	li	v0,0x1
@@NotMatched:
	jr	ra
	li	v0,0

HACK_00:
	addiu t1, a3, -0x1000
	bgez t1, @@Ret
	li	t1, 2
	li	t1, 3
@@Ret:
	j	HACK_00_RETURN
	nop
.endarea
; Clear the relocation entry for the jump at 0x0881A990 (4th instruction in the original subroutine)
; Can be worked around, but it's safer this way.  
.orga 0x1518D4
	.word 0x0


; menu glyph spacing, depending (somewhat) on scale
.org 0x08866908
.area 4*2
	;li	t1, 2	;<-original
	j	HACK_00  ; uses free space from a different subroutine
	li	t2, 2
HACK_00_RETURN:
.endarea
; do not multiply the value by 2
.org 0x08866570
	sll fp, t1, 0


; Increases the size of the glyph buffer for choice lines from 22 to 44
; (Caused some choice lines to be overwritten by the following ones)
.org 0x0881FE54
.area 4*2, 0
	sll	v0,a2,0x6
	sll	a2,a2,0x2
.endarea

.close
