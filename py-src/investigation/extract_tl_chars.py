#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this script was used to generate a chinese text blob of init.bin and BOOT, which I later used to generate a list of characters for the font

import sys
import re
from os import listdir
from os import path
from collections import namedtuple
from collections import deque

import r11

def readlines_utf8_crop_crlf(filepath):
  with open(filepath, "r", encoding="utf-8-sig") as f:
    return [l.rstrip('\r\n') for l in f.readlines()]

def main():
  # # CN
  initbin = path.dirname(__file__) + "/../../text/other-psp-cn/init.bin.full.utf8.txt"
  saveTo = path.dirname(__file__) + "/../../text/tmp/cn-text-utf8/initbin.txt"
  # initbin = path.dirname(__file__) + "/../../text/other-psp-cn/BOOT.BIN.psp.txt"
  # saveTo = path.dirname(__file__) + "/../../text/tmp/cn-text-utf8/boot.txt"
  
  tlTexts = []
  jpTexts = []

  init_lines = readlines_utf8_crop_crlf(initbin)
  
  # init.bin txt content starts from line 2
  init_lines = init_lines[2:]

  init_lines = list(filter(lambda l: not l.startswith("#"), init_lines))
  for i in range(0, len(init_lines), 2):
    jpLine: str = init_lines[i]
    tlLine: str = init_lines[i+1]
    if jpLine.startswith(";dupe") or jpLine.startswith(";unused") or not jpLine.startswith(";"):
      exit("Line {} unexpected text. {}".format(i, jpLine))
    
    # ignore dupes and explicitly unused stuff
    if tlLine.startswith(";dupe") or tlLine.startswith(";unused"):
      continue
    
    if tlLine == "":
      jpText = jpLine.split(";", 3)[3]
      jpTexts.append(jpText)
    else:
      tlTexts.append(tlLine)

  #
  print("tlTexts", len(tlTexts), "jpTexts", len(jpTexts))

  cjkJpFontChars = []
  for jpText in jpTexts:
    jpFontChars = r11.str_to_r11_font_codepoints(jpText)
    cjkJpFontChars.extend(filter(lambda j: j >= 1410, jpFontChars))
  print("", cjkJpFontChars)

  with open(saveTo, "w", encoding="utf-8-sig") as f:
    f.write("".join(tlTexts))



if __name__ == '__main__':
  main()
