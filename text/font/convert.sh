#!/bin/sh

# The png files for fonts must be greyscale and have a bit depth of 2.
# This script below helps to batch-convert any png to proper format using ImageMagick 'convert' tool.
# Use it on your fonts or just for reference.

# imagemagick version 7 is recommended

# input files directory
SRC="glyphs"
TGT="glyphs-new"

mkdir -p $TGT

# outputs to glyphs-new/
ls $SRC | xargs -I{} convert "$SRC/{}" -colorspace Gray -depth 2 -define png:bit-depth=2 -define png:exclude-chunks=date,time $TGT/{}
