#!/bin/sh

./compile.sh && \
./unpack-iso.sh && \
./unpack-afs.sh && \
(cd text && ./1_extract-jap-scenes.sh) && \
./repack-all.sh
