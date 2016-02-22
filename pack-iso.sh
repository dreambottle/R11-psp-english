#!/bin/bash
# Files produced by mkisofs/genisoimage fail to start on psp, but are ok for
# an emulator, or for testing via usb.

# For a release version which will launch on psp, use umdgen, or write your own tool :P .

mkisofs -iso-level 4 -A "PSP GAME" -V "R11" -sysid "PSP GAME" -P "dreambottle" -o iso/r11-repacked.iso iso_extracted/
