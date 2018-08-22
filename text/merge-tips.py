#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from os import listdir
from collections import namedtuple
from collections import deque

debug = True

tips_folderpath = "psp-tips/"
tips_titles = "other-psp/Tips.titles.txt"
tips_order = "other-psp/tips.order.psp.txt"
mergewith = "other-psp/init.psp.txt"
saveas = "other-psp/init.psp.txt"
# saveas = "tips.init.psp.txt"

Tip = namedtuple("Tip", "i, filename, ipsp, jpname, enname, paragraphs")

def prepare_sjis_conv(str):
#         %w|301C FF5E|, # WAVE DASH            => FULLWIDTH TILDE
#         %w|2212 FF0D|, # MINUS SIGN           => FULLWIDTH HYPHEN-MINUS
#         %w|00A2 FFE0|, # CENT SIGN            => FULLWIDTH CENT SIGN
#         %w|00A3 FFE1|, # POUND SIGN           => FULLWIDTH POUND SIGN
#         %w|00AC FFE2|, # NOT SIGN             => FULLWIDTH NOT SIGN
#         %w|2014 2015|, # EM DASH              => HORIZONTAL BAR
#         %w|2016 2225|, # DOUBLE VERTICAL LINE => PARALLEL TO
  str = str.replace("\u2163", "\ufa4d") # Roman numeral IV
  str = str.replace("\u2014", "\u2015") # emdash
  str = str.replace("\u2015\u2015", "\u2015") # double->single dash
  str = str.replace("\uff5e", "\u301c") # Two versions of tilde ～, but the 2nd one can be converted to sjis
  str = str.replace("\u00f6", "o") # ö => o
  str = str.replace("\u014d", "o") # ō => o
  str = str.replace("\u00e9", "e") # é => e
  str = str.replace("''I''", "%CFF8FI%CFFFF") # Yellow-colored I
  return str

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
  if debug: print("Reading TIP files")
  titles = deque(titles)
  tips = []
  for i, t in enumerate(tipfiles):
    lines = readlines_in_textfile(tips_folderpath + t)
    
    # The second line in every tip file indicates the jp tip title. Finding its index.
    tip_title = lines[1]
    jpidxname = next(((i, t) for i, t in enumerate(orderjp) if tip_title == t), None) \
            or next(((i, t) for i, t in enumerate(orderjp) if tip_title.startswith(t)))
    
    tip = Tip(i,
              filename = t,
              ipsp = jpidxname[0],
              jpname = jpidxname[1],
              enname = titles.popleft(),
              paragraphs = [])

    if debug:
      print("Processing TIP PC#%s (%s), PSP#%s: \"%s\"/\"%s\""%(i, t, tip.ipsp, tip.enname, tip.jpname))

    translation_start_index = lines.index("<pre>") + 1
    translated_lines = lines[translation_start_index:]
    translated_lines.append("")
    tip_paragraph = ""
    tip_paragraph_i = 0
    for line in translated_lines:
      if line.startswith("#") or line.startswith("//"):
        continue

      line = line.rstrip()
      
      if (line):
        if len(tip_paragraph) > 1 and not tip_paragraph[-2] == "%":
          tip_paragraph += " "
        tip_paragraph += line.rstrip()
      # An empty line will trigger appending of the last entry
      else:
        if (tip_paragraph):
          tip_paragraph_i += 1
          # %P can't be used here
          tip_paragraph = tip_paragraph.replace("%P", "%N")
          tip.paragraphs.append(tip_paragraph)
          tip_paragraph = ""

    tips.append(tip)

  tips = sorted(tips, key=lambda tip: tip.ipsp)
  if debug:
    print("Analyzing overflows.")
    overflows = 0

    for tip in tips:
      for p_i, p in enumerate(tip.paragraphs):
        if len(p) >= 480:
          overflows += 1
          print('Buffer overflow! Tip PSP#%s (%s) "%s"/"%s", P#%s len: %s'%(tip.ipsp, tip.filename, tip.enname, tip.jpname, p_i+1, len(p)))
          # print(p)

    print("Overflows found: %s"%(overflows))
    print("Merging translated TIPS lines with init.psp.txt file")
  
  f_tips = open(mergewith, "r+b")
  tips_inittxt_lines = f_tips.readlines()
  f_tips.close()
  
  # Hardcode. Change this if required
  tipstart = 7343 #line, starting from 0
  # tipsend = 8110
  
  i = tipstart+1
  for tip in tips:
    if debug: print(tip.ipsp, "(pc:%d)"%(tip.i+1), tip.enname, tip.jpname)
    tips_inittxt_lines[i] = tip.enname.encode("shift_jis_2004") + b'\n'

    if (not tips_inittxt_lines[i-1].endswith(tip.jpname.encode("shift_jis_2004")+b'\n') #, "backslashreplace"
        and tip.ipsp!=37 and not 102>=tip.ipsp>=92):
      print("Mismatch!", tip.jpname, "not in the one of", tips_inittxt_lines[i-1].decode("shift_jis_2004")) #, "replace"
      break
    
    i += 2
    for paragraph in tip.paragraphs:
      tips_inittxt_lines[i] = prepare_sjis_conv(paragraph).encode("shift_jis_2004") + b'\n' #, "backslashreplace"
      i += 2

  # Write modified lines
  with open(saveas, "wb") as f_out:
    for l in tips_inittxt_lines:
      f_out.write(l)


if __name__ == '__main__':
  main()