#!/bin/sh

# extract iso and afs packages and run prepare-texts.sh before running this

mkdir -p tmp/mac-ja-psp/
mkdir -p tmp/mac-combined-psp/
for i in ../mac/[A-Z0-9]*_[0-9]*.SCN ; do
	f=`basename $i .SCN`
	echo "Extracting scene $f text"
	# process translation files
	../bin/extract_scene_text ../mac/$f.SCN tmp/mac-ja-psp/$f.txt & WAITPIDS="$! $WAITPIDS" #|| exit 1;
done
wait $WAITPIDS &>/dev/null
echo "Done."
