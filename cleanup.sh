#!/bin/sh

rm -rf mac/ etc/ iso_extracted/ mac-en/
#rm -f mac-en/*{.SCN,.BIP}
rm -f compressbip decompressbip repack_afs repack_scene extract_scene_text
rm -f workdir/{mac.afs,etc.afs,init.*,BOOT.BIN*}
rm -rf text/{mac-ja-psp,mac-combined-psp,mac-en-only}