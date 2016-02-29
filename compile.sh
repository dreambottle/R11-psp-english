#!/bin/bash
SRC=./src

CFLAGS="-std=c99"

gcc $CFLAGS -o extract_scene_text $SRC/extract_scene_text.c || exit 1;
gcc $CFLAGS -o repack_afs $SRC/repack_afs.c
gcc $CFLAGS -o repack_scene $SRC/repack_scene.c
gcc $CFLAGS -o decompressbip $SRC/decompressbip.c $SRC/lzss.c
gcc $CFLAGS -o compressbip $SRC/compressbip.c $SRC/lzss.c
