#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re

def main():
  # Standard psp engine limit is 480
  warn_chars_buffer_overflow = 480;
  warn_chars_screen = 400;
  warn_chars_line = 45*4;

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
          line = line.replace(seq, "", 1);

      if ("%" in line):
        # % sequence wasn't cut out for some reason
        print (i, ":", line, ':', allseq)

      chars+=len(line)
      lines+=1;
      if (chars > warn_chars_screen):
        overflowTxt = " May cause buffer overflow!" \
                  if (chars > warn_chars_buffer_overflow) else ""
        print("Line %d: %d chars in last %d lines.%s"
              % (i, chars, lines, overflowTxt))
        if (overflowTxt != ""): print ("'%s'" % line)
      # if (len(line) > warn_chars_line):
      #   print(("Line  %d: %d chars on the line!") % (i, len(line)))



if __name__ == '__main__':
  main();
