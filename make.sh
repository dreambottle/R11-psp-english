#!/bin/sh

./compile.sh && \
./unpack-iso.sh && \
./unpack-afs.sh && \
(cd text && ./1_extract-jap-scenes.sh && ./2_prepare-texts.sh) && \
./pack-afs.sh && \
./pack-iso.sh
