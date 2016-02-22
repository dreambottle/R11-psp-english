#!/bin/sh

# extract iso and afs packages and run prepare-texts.sh before running this

mkdir -p mac-ja-psp/
mkdir -p mac-combined-psp/
for i in ../mac/[A-Z0-9]*_[0-9]*.SCN ; do
	f=`basename $i .SCN`
	echo Extracting $f scene
	# process translation files
	../extract_scene_text ../mac/$f.SCN mac-ja-psp/$f.txt || exit 1;
done