#!/bin/sh
set -euo pipefail

rm -rf r11_mac/ r11_etc/ r11_iso_extracted/ r11_mac_en/ r11_etc_en/
rm -rf bin/
rm -f workdir/{mac.afs,etc.afs,init.*,BOOT.BIN*}
rm -rf text/tmp/{mac-jp-psp,mac-en-combined-psp,mac-cn-combined-psp}
rm -rf text/tmp
rm -f text/font/FONT00.{FNT,mod}
