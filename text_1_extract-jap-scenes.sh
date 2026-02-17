#!/bin/sh
set -euo pipefail

# Extracts text from scenes (aka chapters, main text) to text files with the original encoding.
# Before running this, iso and afs packages must be unpacked, so that .SCN files are present in r11_mac/ folder.

mkdir -p text/tmp/mac-jp-psp/
for i in r11_mac/[A-Z0-9]*_[0-9]*.SCN ; do
	f=`basename $i .SCN`
	echo "Extracting scene $f text"
	# process translation files
	# ./bin/extract_scene_text r11_mac/$f.SCN tmp/mac-jp-psp/$f.txt & WAITPIDS="$! $WAITPIDS"
	./bin/extract_scene_text r11_mac/$f.SCN text/tmp/mac-jp-psp/$f.txt || exit 1;
done
# wait $WAITPIDS &>/dev/null
echo "Done."
