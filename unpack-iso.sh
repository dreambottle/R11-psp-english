#!/bin/bash

ISO_FILE=iso/Remember11-jap.iso

#isoinfo -f -i iso/Remember11-jap.iso | nl -nln -s ";" | awk -F ";" '{print substr($2,2) " -" $1}' > iso/sort_file
echo "Extracting ISO."
7z x $ISO_FILE -oiso_extracted/

