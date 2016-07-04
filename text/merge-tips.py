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

def fix_sjis(bstr):
#         %w|301C FF5E|, # WAVE DASH            => FULLWIDTH TILDE
#         %w|2212 FF0D|, # MINUS SIGN           => FULLWIDTH HYPHEN-MINUS
#         %w|00A2 FFE0|, # CENT SIGN            => FULLWIDTH CENT SIGN
#         %w|00A3 FFE1|, # POUND SIGN           => FULLWIDTH POUND SIGN
#         %w|00AC FFE2|, # NOT SIGN             => FULLWIDTH NOT SIGN
#         %w|2014 2015|, # EM DASH              => HORIZONTAL BAR
#         %w|2016 2225|, # DOUBLE VERTICAL LINE => PARALLEL TO
  bstr = bstr.replace(b"\u2163", b"\xfa\x4d") # Roman numeral IV
  bstr = bstr.replace(b"\u301c", b"\xff\x5e")
  bstr = bstr.replace(b"\u2014", b"\x20\x15")
  bstr = bstr.replace(b"\\xf6", b"o") # ö => o
  bstr = bstr.replace(b"\\xe9", b"e") # é => e
  bstr = bstr.replace(b"''I''", b"%CFF8FI%CFFFF") # Yellow-colored I
  return bstr;

def readlines_in_textfile(filepath):
  with open(filepath, "r", encoding="UTF-8") as f:
    return [l.rstrip('\r\n') for l in f.readlines()]

def main():
  titles = readlines_in_textfile(tips_titles)

  tipfiles = listdir(tips_folderpath)
  tipfiles.sort()
  if (len(titles) != len(tipfiles)):
    exit("tips count mismatch")
  
  orderjp = readlines_in_textfile(tips_order)

  # read all tip files
  titles = deque(titles)
  tips = []
  for i, t in enumerate(tipfiles):
    lines = readlines_in_textfile(tips_folderpath + t)
    
    # The second line in every tip file indicates the jp tip title. Finding its index.
    tip_title = lines[1]
    jpidxname = next(((i, t) for i, t in enumerate(orderjp) if tip_title == t), None) \
            or next(((i, t) for i, t in enumerate(orderjp) if tip_title.startswith(t)))
    
    tip = Tip(i, ipsp = jpidxname[0],
               jpname = jpidxname[1],
               enname = titles.popleft(),
               lines = [])

    enstart = lines.index("<pre>") + 1;
    enlines = lines[enstart:]
    # An empty line to trigger appending of the last entry
    enlines.append("")
    tipline = ""
    for line in enlines:
      if (line and not line.startswith("#")):
        if len(tipline) > 1 and not tipline[-2] == "%":
          tipline += " "
        tipline += line.rstrip()
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
      print("mismatch!", tip.jpname, tipslines[i-1].decode("SJIS", "replace"))
      break
    
    i += 2
    for line in tip.lines:
      tipslines[i] = fix_sjis(line.encode("SJIS", "backslashreplace")) + b'\n'
      i += 2

  # Write modified lines
  with open(saveas, "wb") as f_out:
    for l in tipslines:
      f_out.write(l)


if __name__ == '__main__':
  main();