#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

def main():
  warn_chars_screen = 330;
  warn_chars_line = 38*4;

  fdir = "mac-en-only/"
  files = os.listdir(fdir);

  for fname in files:
    f = open(fdir+fname, "r", encoding="SJIS")
    lns = f.readlines()
    f.close()
    print(fname)

    chars = 0;
    lines = 0;
    clear = True;

    for i, line in enumerate(lns):
      if clear:
        clear=False
        chars=0
        lines=0

      line = line[:-1] # strip \n
      allseq = re.findall("(?:%[KkPpNnOV]|%T\d\d|%C[\dA-F]{4}|%X\d{3}|%TS\d{3}|%TE|%F[SE]|%L[CLR])+", line);
      if (allseq):
        if allseq[-1].endswith("%P") or allseq[-1].endswith("%p"):
          clear = True;
        for seq in allseq:
          line = line.replace(seq, "");

      # else:
      #   print("No sequences at line", i)

      if ("%" in line):
        print (i, ":", line)

      chars+=len(line)
      lines+=1;
      if (chars > warn_chars_screen):
        print("Line %d: %d chars in last %d lines. May cause buffer overflow!"
          % (i, chars, lines) )
      # if (len(line) > warn_chars_line):
      #   print(("Line  %d: %d chars on the line!") % (i, len(line)))



if __name__ == '__main__':
  main();
