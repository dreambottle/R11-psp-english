#!/bin/sh

./compile.sh && \
./unpack-iso.sh && \
./unpack-afs.sh && \
./text_1_extract-jap-scenes.sh && \
./repack-all.sh
