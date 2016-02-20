.psp
.relativeinclude on

.open "../workdir/BOOT.BIN", "../workdir/BOOT.BIN.patched", 0x0

//757C
.orga 0x761c
.area 4
li a0, 1
.endarea



.orga 0x7624
.area 4
li a1, 1
.endarea

.close
