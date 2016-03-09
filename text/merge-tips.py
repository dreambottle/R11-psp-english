#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from os import listdir
from collections import namedtuple
from collections import deque

tips_folderpath = "psp-tips/"
tips_titles = "other-psp/Tips.titles.txt"
tips_order = "other-psp/tips.order.psp.txt"
mergewith = "other-psp/init.psp.txt"
saveas = "tips.init.psp.txt"

Tip = namedtuple("Tip", "i, ipsp, jpname, enname, lines")

def fixsjis(bstr):
#         %w|301C FF5E|, # WAVE DASH            => FULLWIDTH TILDE
#         %w|2212 FF0D|, # MINUS SIGN           => FULLWIDTH HYPHEN-MINUS
#         %w|00A2 FFE0|, # CENT SIGN            => FULLWIDTH CENT SIGN
#         %w|00A3 FFE1|, # POUND SIGN           => FULLWIDTH POUND SIGN
#         %w|00AC FFE2|, # NOT SIGN             => FULLWIDTH NOT SIGN
#         %w|2014 2015|, # EM DASH              => HORIZONTAL BAR
#         %w|2016 2225|, # DOUB
  bstr = bstr.replace(b"\u2163", b"\xfa\x4d") # Roman numeral IV
  bstr = bstr.replace(b"\u301c", b"\xff\x5e")
  bstr = bstr.replace(b"\u2014", b"\x20\x15")
  bstr = bstr.replace(b"\\xf6", b"o") # ö => o
  bstr = bstr.replace(b"\\xe9", b"e") # é => e
  bstr = bstr.replace(b"''I''", b"%CFF8FI%CFFFF") # Yellow-colored I
  return bstr;


def main():

  f_titles = open(tips_titles, "r", encoding="UTF-8")
  titles = [x.rstrip('\r\n') for x in f_titles.readlines()]
  f_titles.close()
  
  tipfiles = listdir(tips_folderpath)
  tipfiles.sort()
  if (len(titles) != len(tipfiles)):
    exit("tips count mismatch")
  
  f = open(tips_order, "r", encoding="UTF-8")
  orderjp = [l.rstrip('\r\n') for l in f.readlines()]
  f.close()

  # read all tip files
  titles = deque(titles)
  tips = []
  for i, t in enumerate(tipfiles):
    f = open(tips_folderpath + t, "r", encoding="UTF-8")
    lines = [l.rstrip('\r\n') for l in f.readlines()]
    f.close()
    
    # The second line in every tip file indicates the jp tip title
    jpidxname = next(((i, t) for i, t in enumerate(orderjp) if lines[1] == t), None) \
            or next(((i, t) for i, t in enumerate(orderjp) if lines[1].startswith(t)))
    
    tip = Tip(i, ipsp = jpidxname[0],
               jpname = jpidxname[1],
               enname = titles.popleft(),
               lines = [])

    enstart = lines.index("<pre>") + 1;
    enlines = lines[enstart:]
    # An empty line to ensure that the last entry is always appended
    enlines.append("")
    tipline = ""
    for line in enlines:
      if (line and not line[0].startswith("#")):
        # if not tipline.endswith("%N"):
        #   tipline += " "
        tipline += line
      elif (tipline):
        tip.lines.append(tipline)
        tipline = ""

    tips.append(tip)

  tips = sorted(tips, key=lambda tip: tip.ipsp)
  # print(tips)
  
  f_tips = open(mergewith, "r+b")
  tipslines = f_tips.readlines()
  f_tips.close()
  
  # Hardcode. Change this if required
  tipstart = 7344
  tipsend = 8110
  
  i = tipstart+1
  for tip in tips:
    print(tip.ipsp, "(pc:%d)"%(tip.i+1), tip.enname, tip.jpname)
    tipslines[i] = tip.enname.encode("SJIS") + b'\n'
    
    if (not tipslines[i-1].endswith(tip.jpname.encode("SJIS", "backslashreplace")+b'\n')
        and tip.ipsp!=37 and not 102>=tip.ipsp>=92):
      print("mismatch!", tip.jpname, tipslines[i-1].decode("SJIS", "backslashreplace"))
      break
    
    i += 2
    for line in tip.lines:
      tipslines[i] = fixsjis(line.encode("SJIS", "backslashreplace")) + b'\n'
      i += 2
    
  f_out = open(saveas, "wb")
  for l in tipslines:
    f_out.write(l)
  f_out.close()

if __name__ == '__main__':
  main();