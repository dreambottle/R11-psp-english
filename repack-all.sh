#!/bin/sh
set -euo pipefail

./text_2_prepare-texts.sh && \
./pack-afs.sh && \
./pack-iso.sh
