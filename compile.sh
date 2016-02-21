#!/bin/bash
SRC=./src
gcc -std=c99 -o extract_scene_text $SRC/extract_scene_text.c || exit 1;
gcc -o repack_afs $SRC/repack_afs.c
gcc -o repack_scene $SRC/repack_scene.c
gcc -o decompressbip $SRC/decompressbip.c $SRC/lzss.c
gcc -o compressbip $SRC/compressbip.c $SRC/lzss.c
