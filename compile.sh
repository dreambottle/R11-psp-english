#!/bin/bash
SRC=./src
gcc -o repack_afs $SRC/repack_afs.c
gcc -o repack_scene $SRC/repack_scene.c
gcc -o decompressbip $SRC/decompressbip.c
gcc -o compressbip $SRC/compressbip.c
