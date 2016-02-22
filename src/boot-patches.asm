.psp
.relativeinclude on

.open "../workdir/BOOT.BIN.patched", 0x0

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
li a1, 1
.endarea

.close
