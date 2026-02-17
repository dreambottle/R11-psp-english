#!/bin/bash
set -euo pipefail

SRC=./src

CFLAGS="-std=c99 -O2"

mkdir -p bin
gcc $CFLAGS -o bin/extract_scene_text $SRC/extract_scene_text.c || exit 1;
gcc $CFLAGS -o bin/repack_afs $SRC/repack_afs.c
gcc $CFLAGS -o bin/repack_scene $SRC/repack_scene.c
gcc $CFLAGS -o bin/decompressbip $SRC/decompressbip.c $SRC/lzss.c
gcc $CFLAGS -o bin/compressbip $SRC/compressbip.c $SRC/lzss.c
