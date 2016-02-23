#!/bin/sh

(cd text && ./2_prepare-texts.sh)
./pack-afs.sh
./pack-iso.sh
