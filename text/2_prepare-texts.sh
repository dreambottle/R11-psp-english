#!/bin/sh

# The source text for this script is located in chapters-psp/.
# This script processes chapters-psp/ further, preparing the TL to be in the format, digestible by repack_scene tool.

# set to "en" if unset
if [ -z "${TL_SUFFIX}" ]; then
    export TL_SUFFIX="en"
fi

merge_translation () {
	# python3 ../py-src/translation_preproc.py -i chapters-psp/$1.txt -o tmp/mac-${TL_SUFFIX}-only/$1.txt -t ${TL_SUFFIX} --onlytl || exit 1;
	python3 ../py-src/translation_preproc.py -i chapters-psp/$1.txt -o tmp/mac-${TL_SUFFIX}-combined-psp/$1.txt -t ${TL_SUFFIX} || exit 1;
}

mkdir -p tmp/mac-${TL_SUFFIX}-only/
mkdir -p tmp/mac-${TL_SUFFIX}-combined-psp/
WAITPIDS=""
for i in chapters-psp/[A-Z0-9]*_[0-9]*.txt ; do
	f=`basename $i .txt`
	echo "Preparing chapter: $i"
	merge_translation $f #& WAITPIDS="$WAITPIDS $!"
done

wait $WAITPIDS &> /dev/null
