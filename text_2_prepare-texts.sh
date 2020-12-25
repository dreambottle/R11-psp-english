#!/bin/sh

# The source text for this script is located in chapters-psp/.
# This script processes chapters-psp/ further, preparing the TL to be in the format, digestible by repack_scene tool.

# set to "en" if unset
if [ -z "${TL_SUFFIX}" ]; then
    export TL_SUFFIX="en"
fi

prepare_translation () {
	python3 ./py-src/translation_preproc.py -i text/chapters-psp/$1.txt -o text/tmp/mac-${TL_SUFFIX}-combined-psp/$1.txt -t ${TL_SUFFIX} || exit 1;
}

mkdir -p text/tmp/mac-${TL_SUFFIX}-combined-psp/
WAITPIDS=""
for i in text/chapters-psp/[A-Z0-9]*_[0-9]*.txt ; do
	f=`basename $i .txt`
	echo "Preparing chapter: $i"
	prepare_translation $f #& WAITPIDS="$WAITPIDS $!"
done

wait $WAITPIDS &> /dev/null
