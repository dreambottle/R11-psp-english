#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import listdir
from collections import namedtuple
from collections import deque

tips_folderpath = "www-tips/"
tips_titles = "other-psp/Tips.titles.txt"
mergewith = "other-psp/init.bin.psp.txt"
saveas = "tips.init.psp.txt"

Tip = namedtuple("Tip", "i, jpname, enname, lines")

def main():

  f_titles = open(tips_titles, "r", encoding="UTF-8")
  titles = [x.rstrip('\r\n') for x in f_titles.readlines()]
  f_titles.close()
  
  tipfiles = listdir(tips_folderpath)
  tipfiles.sort()
  if (len(titles) != len(tipfiles)):
    exit("tips count mismatch")

  titles = deque(titles)
  tips = []
  for i, t in enumerate(tipfiles):
    f = open(tips_folderpath + t, "r", encoding="UTF-8")
    lines = [l.strip('\r\n') for l in f.readlines()]
    f.close()

    tip = Tip(i, jpname = lines[1],
               enname = titles.popleft(),
               lines = [])

    enstart = lines.index("<pre>") + 1;
    enlines = lines[enstart:]
    # An empty line to make the last entry always be appended
    enlines.append("")
    tipline = ""
    for line in enlines:
      if (line):
        # if not tipline.endswith("%N"):
        #   tipline += " "
        tipline += line
      elif (tipline):
        tip.lines.append(tipline)
        tipline = ""

    tips.append(tip)

  print(tips)
  

if __name__ == '__main__':
  main();