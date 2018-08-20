#!/bin/sh

# The text in www* folders was copied to chapters-psp/ and edited because of mismatches between pc and psp versions.
# extract_en.pl extracts the english lines from the raw translation file, changes encoding, converts unsupported characters etc.
# This allows a less painful further processing and insertion into scenes.

# Shift-JIS reference tables
# https://msdn.microsoft.com/en-us/goglobal/cc305152.aspx

# Dependencies: Perl File::Slurp module.
# > cpan File::Slurp

merge_translation () {
	# process special characters and remove unimportant lines
	# ./extract_en.pl chapters-psp/$1.txt > mac-en-only/$1.txt || exit 1; # deprecated
	./translation_preproc.py chapters-psp/$1.txt > mac-en-only/$1.txt || exit 1;
	# combine with my format
	./merge-scene-lines.py mac-ja-psp/$1.txt mac-en-only/$1.txt mac-combined-psp/$1.txt || exit 1;
}

mkdir -p mac-en-only/
WAITPIDS=""
for i in chapters-psp/[A-Z0-9]*_[0-9]*.txt ; do
	f=`basename $i .txt`
	echo Processing translation: $i
	merge_translation $f & WAITPIDS="$WAITPIDS $!"
done

wait $WAITPIDS &> /dev/null
