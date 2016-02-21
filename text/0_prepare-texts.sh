#!/bin/sh

# The text in www* folders has to be processed to allow further insertion into scenes.
# This includes removing all unneeded stuff(comments, jap lines), converting characters where needed etc.
# Also, the initial text, downloaded from tlwiki, was pulled from the pc version.

# It has some minor mismatches with psp version, so they need to be addressed as well.

# Shift-JIS reference tables
# https://msdn.microsoft.com/en-us/goglobal/cc305152.aspx
# 

# Dependencies: Perl File::Slurp module.
# > cpan File::Slurp

mkdir -p mac-en-only/
for i in chapters-psp/[A-Z0-9]*_[0-9]*.txt ; do
	echo $i
	f=`basename $i .txt`
    ./extract_en.pl $i > mac-en-only/$f.txt || exit 1;
done
