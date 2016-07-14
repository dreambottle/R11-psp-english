.psp
.relativeinclude off

.open "BOOT.BIN.patched", 0x08803F60

//757C
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

.close
