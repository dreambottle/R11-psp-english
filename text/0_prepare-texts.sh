#!/bin/sh

# The text in www* folders was copied to chapters-psp/ and edited because of mismatches between pc and psp versions.
# extract_en.pl extracts the english lines from the raw translation file, changes encoding, converts unsupported characters etc.
# This allows a less painful further processing and insertion into scenes.

# Shift-JIS reference tables
# https://msdn.microsoft.com/en-us/goglobal/cc305152.aspx

# Dependencies: Perl File::Slurp module.
# > cpan File::Slurp

mkdir -p mac-en-only/
for i in chapters-psp/[A-Z0-9]*_[0-9]*.txt ; do
	echo $i
	f=`basename $i .txt`
    ./extract_en.pl $i > mac-en-only/$f.txt || exit 1;
done
