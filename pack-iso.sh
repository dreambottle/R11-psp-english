#!/bin/bash
# -sort iso/sort_file
mkisofs -iso-level 4 -A "PSP GAME" -V "R11" -sysid "PSP GAME" -P "dreambottle" -o iso/r11-repacked.iso iso_extracted/