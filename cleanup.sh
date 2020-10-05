#!/bin/sh

rm -rf r11_mac/ r11_etc/ r11_iso_extracted/ r11_mac_en/ r11_etc_en/
rm -rf bin/
rm -f workdir/{mac.afs,etc.afs,init.*,BOOT.BIN*}
rm -rf text/tmp/{mac-ja-psp,mac-en-combined-psp,mac-en-only,mac-cn-combined-psp,mac-cn-only}
rm -rf text/tmp
rm -f text/font/FONT00.{FNT,mod}
