#!/bin/bash

mkisofs -iso-level 4 -xa -A "PSP GAME" -V "R11" -sysid "PSP GAME" -volset "" -p "" -publisher "" -o iso/r11-repacked.iso iso_extracted/
