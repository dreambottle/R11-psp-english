#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from os import listdir
from collections import namedtuple
from collections import deque

debug = True

tips_folderpath = "tips-psp/"
tips_titles = "other-psp/Tips.titles.txt"
tips_order = "other-psp/tips.order.psp.txt"
mergewith = "other-psp/init.psp.txt"
# saveas = "other-psp/init.psp.txt"
saveas = "tips.init.psp.txt"

# Was used to convert old format of TIPS to a new one.
# Only keeping the code for reference, it is now obsolete.
convert2dir = None
# convert2dir = "tips-psp2/"

Tip = namedtuple("Tip", "i_psp, i_pc, filename, jpname, enname, jpparagraphs, paragraphs")

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
    exit("tips count mismatch; files: %s, titles: %s"%(len(tipfiles), len(titles)))
  
  orderjp = readlines_in_textfile(tips_order)

  # read all tip files
  if debug: print("Reading TIP files")
  # titles = deque(titles)
  tips = []
  for i, t in enumerate(tipfiles):
    lines = readlines_in_textfile(tips_folderpath + t)
    
    # The second line in every tip file indicates the jp tip title. Finding its index.
    tip_jp_title = lines[1]
    jp_idx_name = next(((i, jp_t) for i, jp_t in enumerate(orderjp) if tip_jp_title == jp_t), None)
    
    translated_title = lines[2]

    # 6-th line holds the index of the tip in the PC version
    i_pc = int(lines[5][-3:])

    tip = Tip(filename = t,
              i_pc = i_pc,
              i_psp = jp_idx_name[0],
              jpname = jp_idx_name[1],
              enname = translated_title,
              jpparagraphs = [],
              paragraphs = [])

    if debug:
      print("Processing TIP PC#%s, PSP#%s, (%s): \"%s\"/\"%s\""%(i_pc, tip.i_psp, t, tip.enname, tip.jpname))

    translation_start_index = lines.index("#PARAGRAPHS_TRANSLATED:") + 1
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

  tips = sorted(tips, key=lambda tip: tip.i_psp)
  if debug:
    print("Analyzing overflows.")
    overflows = 0

    for tip in tips:
      for p_i, p in enumerate(tip.paragraphs):
        if len("".join(p.split("%N"))) > 480:
          overflows += 1
          print('Buffer overflow! Tip PSP#%03d (%s) "%s"/"%s", P#%s len: %s'%(tip.i_psp, tip.filename, tip.enname, tip.jpname, p_i+1, len(p)))
          # print(p)

    print("Overflows found: %s"%(overflows))
    print("Merging translated TIPS lines with init.psp.txt file")
  
  f_tips = open(mergewith, "r+b")
  tips_inittxt_lines = f_tips.readlines()
  f_tips.close()
  
  # Hardcode. Change this if required
  tips_start = 7343 #line, starting from 0
  # tips_end = 8110
  
  # current line pointer
  cur = tips_start
  
  for tip in tips:
    if debug: print("Merging %03d"%(tip.i_psp), "(pc:%03d)"%(tip.i_pc), tip.enname, tip.jpname)
    tips_inittxt_lines[cur + 1] = tip.enname.encode("shift_jis_2004") + b'\n'

    if (not tips_inittxt_lines[cur].endswith(tip.jpname.encode("shift_jis_2004")+b'\n')):
      print("Mismatch!", tip.jpname, "not found, instead got:", tips_inittxt_lines[cur].decode("shift_jis_2004"))
      break

    # if convert2dir:
    #   jp_title_line = tips_inittxt_lines[cur].decode("shift_jis_2004")
    #   tip_start_addr = jp_title_line.split(";")[1]
    #   jp_title = jp_title_line.split(";")[3].rstrip()

    # move pointer to first paragraph
    cur += 2
    for p_i, paragraph in enumerate(tip.paragraphs):
      tips_inittxt_lines[cur + 1] = prepare_sjis_conv(paragraph).encode("shift_jis_2004") + b'\n'
      tip.jpparagraphs.append(tips_inittxt_lines[cur].decode("shift_jis_2004").rstrip())
      cur += 2

    # if convert2dir:
    #   with open("%sTIP%03d.txt"%(convert2dir, tip.i_psp), "w") as newtip_out:
    #     newtip_out.write("TIP%03d\n"%(tip.i_psp))
    #     newtip_out.write("%s\n"%(jp_title))
    #     newtip_out.write("%s\n"%(tip.enname))
    #     newtip_out.write("paragraph_count:%d\n"%(len(tip.paragraphs)))
    #     newtip_out.write("init_addr:%s\n"%(tip_start_addr))
    #     newtip_out.write("pc_index:TIP_%03d\n"%(tip.i_pc))

    #     newtip_out.write("\n")
    #     newtip_out.write("#PARAGRAPHS_JP:\n")
    #     for p_i, paragraph in enumerate(tip.jpparagraphs):
    #       newtip_out.write("#JP#%s\n"%(p_i+1))
    #       jp_paragraph_multiline = "%N\n".join(paragraph.split("%N"))
    #       newtip_out.write("%s\n"%(jp_paragraph_multiline))
    #       if not jp_paragraph_multiline.endswith("\n"): newtip_out.write("\n")

    #     newtip_out.write("\n")
    #     newtip_out.write("#PARAGRAPHS_TRANSLATED:\n")
    #     for p_i, paragraph in enumerate(tip.paragraphs):
    #       newtip_out.write("#EN#%s\n"%(p_i+1))
    #       en_paragraph_multiline = "%N\n".join(paragraph.split("%N"))
    #       newtip_out.write("%s\n"%(en_paragraph_multiline))
    #       if not en_paragraph_multiline.endswith("\n"): newtip_out.write("\n")
    #     newtip_out.flush()


  # Write modified lines
  with open(saveas, "wb") as f_out:
    for l in tips_inittxt_lines:
      f_out.write(l)


if __name__ == '__main__':
  main()
