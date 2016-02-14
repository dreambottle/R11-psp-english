#!/bin/bash

ISO_FILE=iso/Remember11-jap.iso

echo "Getting file soring order"
#isoinfo -f -i iso/Remember11-jap.iso | nl -nln -s ";" | awk -F ";" '{print substr($2,2) " -" $1}' > iso/sort_file
#mkdir extracted #not required
7z x $ISO_FILE -oiso_extracted/

mkdir working_copy
cp iso_extracted/PSP_GAME/SYSDIR/BOOT.BIN working_copy/BOOT.BIN