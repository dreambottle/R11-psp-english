#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script can be used to apply the text from TIPS in `tips-psp/` to `other-psp-*/init.bin.utf8.txt` file
# Example usage: `python3 py-src/merge_tips.py cn`

import sys
import re
from os import listdir
from os import path
from collections import namedtuple
from typing import List

import r11

debug = True

tips_folderpath = path.dirname(__file__) + "/../text/tips-psp/"
tips_order = path.dirname(__file__) + "/../text/other-psp-en/tips.order.psp.txt"
# saveas = "tips.init.psp.txt"

# Was used to convert old format of TIPS to a new one.
# Only keeping the code for reference, it is now obsolete.
convert2dir = None
# convert2dir = "tips-psp2/"

Tip = namedtuple("Tip", [
    "filename",
    "i_psp", "i_pc", "init_bin_addr",
    "jptitle", "entitle", "cntitle",
    "jpparagraphs", "enparagraphs", "cnparagraphs"
  ])

# def prepare_sjis_conv(str):
# #         %w|301C FF5E|, # WAVE DASH            => FULLWIDTH TILDE
# #         %w|2212 FF0D|, # MINUS SIGN           => FULLWIDTH HYPHEN-MINUS
# #         %w|00A2 FFE0|, # CENT SIGN            => FULLWIDTH CENT SIGN
# #         %w|00A3 FFE1|, # POUND SIGN           => FULLWIDTH POUND SIGN
# #         %w|00AC FFE2|, # NOT SIGN             => FULLWIDTH NOT SIGN
# #         %w|2014 2015|, # EM DASH              => HORIZONTAL BAR
# #         %w|2016 2225|, # DOUBLE VERTICAL LINE => PARALLEL TO
#   #str = str.replace("\u2163", "\ufa4d") # Roman numeral IV
#   str = str.replace("\u2014", "\u2015") # em dash
#   str = str.replace("\u2015\u2015", "\u2015") # double em dash '——' -> single em dash '—'
#   str = str.replace("\uff5e", "\u301c") # Two versions of tilde ～, but the 2nd one can be converted to sjis
#   str = str.replace("\u00f6", "o") # ö => o
#   str = str.replace("\u00e9", "e") # é => e
#   str = str.replace("''I''", "%CFF8FI%CFFFF") # Yellow-colored I
#   return str

def _append_paragraph(tip_paragraph: str, lang: str, paragraph_id: int, tip: Tip):
  if "%P" in tip_paragraph:
    raise Exception("Tips can't contain a %P sequence")

  if lang == "EN":
    tip.enparagraphs.append(tip_paragraph)
    if tip.enparagraphs.__len__() != paragraph_id:
      print("EN paragraph id mismatch. TIP#{}".format(tip.i_psp))
  elif lang == "CN":
    tip.cnparagraphs.append(tip_paragraph)
    if tip.cnparagraphs.__len__() != paragraph_id:
      print("CN paragraph id mismatch. TIP#{}".format(tip.i_psp))
  else:
    raise Exception("unknown lang %s"%(lang))

def read_tips() -> List[Tip]:
  tipfiles = listdir(tips_folderpath)
  tipfiles.sort()
  
  # this file contains tips in the same order as in init.bin
  orderjp = r11.readlines_utf8_crop_crlf(tips_order)

  # read all tip files
  if debug: print("Reading TIP files")
  tips = []
  for i, t in enumerate(tipfiles):
    # if debug: print("Reading", t)
    lines = r11.readlines_utf8_crop_crlf(tips_folderpath + t)
    
    # The second line in every tip file indicates the jp tip title. Finding its init.bin order.
    tip_jp_title = lines[1]
    en_title = lines[2]
    cn_title = lines[3]
    # Tip titles should be tagged and not rely on line number. For now, keeping this hack and excluding these lines further
    lines = lines[:1] + lines[4:]

    # tuple (<psp index>, <jp title>) or None if doesnt exist. (is it still needed?)
    psp_idx = next(((i, jp_t) for i, jp_t in enumerate(orderjp) if tip_jp_title == jp_t), None)

    # "pc_index:" line holds the index of the tip in the PC version
    i_pc = int(lines[3][-3:])

    init_bin_addr = lines[2][-4:]

    tip = Tip(filename = t,
              i_pc = i_pc,
              i_psp = psp_idx[0],
              init_bin_addr = init_bin_addr,
              jptitle = tip_jp_title,
              entitle = en_title,
              cntitle = cn_title,
              jpparagraphs = [], # its an ugly design, but this won't be initialized here
              enparagraphs = [],
              cnparagraphs = [])

    if debug:
      print("Processing TIP PSP#%s (%s), PC#%s, EN:\"%s\" JP:\"%s\""%(tip.i_psp, tip.filename, i_pc, tip.entitle, tip.jptitle))

    translation_start_index = lines.index("#PARAGRAPHS_TRANSLATED:") + 1
    translated_lines = lines[translation_start_index:]
    translated_lines.append("")
    translation_lang = ""
    tip_paragraph = ""
    tip_paragraph_id = -1

    for line in translated_lines:
      # parse current paragraph index and lang
      if re.match("#[A-Z]{2}#\d+", line):
        # but before that, append last paragraph and reset 
        if (tip_paragraph):
          _append_paragraph(tip_paragraph, translation_lang, tip_paragraph_id, tip)
          tip_paragraph = ""

        translation_lang = line[1:3]
        tip_paragraph_id = int(line[4:])
        # print("Paragraph", translation_lang, tip_paragraph_id)

      # unknown #... lines and //... are considered comments and are skipped
      # empty lines are skipped
      if line.startswith("#") or line.startswith("//") or not line:
        continue

      line = line.rstrip()
      
      # in EN translation add a whitespace between the lines if there is no %N in the end
      if translation_lang == "EN" and len(tip_paragraph) > 1 and not tip_paragraph[-2] == "%":
        tip_paragraph += " "

      tip_paragraph += line
    
    # append last paragraph to tip
    _append_paragraph(tip_paragraph, translation_lang, tip_paragraph_id, tip)

    if tip.enparagraphs.__len__() != tip.cnparagraphs.__len__():
      msg = "Paragraph count mismatch in TIP#{}".format(tip.i_psp)
      print(msg)
      # raise Exception(msg)

    tips.append(tip)

  # should already be sorted because tips are now using psp indexes in filenames. Leaving this here just in case.
  tips = sorted(tips, key=lambda tip: tip.i_psp)
  return tips

def main():
  
  lang_to_merge = sys.argv[1] if sys.argv[1] else "en"

  if lang_to_merge == "en":
    mergewith = path.dirname(__file__) + "/../text/other-psp-en/init.bin.utf8.txt"
    saveas = path.dirname(__file__) + "/../text/other-psp-en/init.bin.utf8.txt"
    # Hardcode. Change this if required.
    # tips_start should point to ";7610;12;ソシオロジィ" line number, starting from 0 (-1 from the line that your editor shows)
    tips_start = 7372
  elif lang_to_merge == "cn":
    mergewith = path.dirname(__file__) + "/../text/other-psp-cn/init.bin.utf8.txt" #CN
    saveas = path.dirname(__file__) + "/../text/other-psp-cn/init.bin.utf8.txt"
    tips_start = 7090
  else:
    raise Exception()


  tips_end = tips_start + 766 # lower boundary line for the tips cursor, exclusive. Also 0-based.
  
  tips = read_tips()

  if debug:
    print("Analyzing overflows (EN TL).")
    overflows = 0

    for tip in tips:
      for p_i, p in enumerate(tip.enparagraphs):
        if len("".join(p.split("%N"))) > 480:
          overflows += 1
          print('Buffer overflow! Tip PSP#%03d (%s) "%s"/"%s", P#%s len: %s'%(tip.i_psp, tip.filename, tip.entitle, tip.jptitle, p_i+1, len(p)))
          # print(p)

    print("Overflows found: %s"%(overflows))
    print("Merging translated TIPS lines with init.psp.txt file")
  
  with open(mergewith, "r", encoding="utf-8-sig") as f:
    tips_inittxt_lines = f.readlines()
  
  # current line cursor
  cur = tips_start
  
  for tip in tips:
    if cur >= tips_end:
      print("Mismatch! Reached the tips end.")
      exit()

    if debug: print("Merging %03d"%(tip.i_psp), "(pc:%03d)"%(tip.i_pc), tip.entitle, tip.jptitle)

    title = tip.cntitle if lang_to_merge == "cn" else tip.entitle
    tips_inittxt_lines[cur + 1] = title + "\n"

    jp_title_split = tips_inittxt_lines[cur].rstrip().split(";", 3)

    if (jp_title_split.__len__() != 4 or jp_title_split[3] != tip.jptitle):
      print("Mismatch! Tip JP title:{} not found, instead got {}".format(tip.jptitle, tips_inittxt_lines[cur].rstrip()))
      exit(1)

    title_init_bin_addr = jp_title_split[1]
    if title_init_bin_addr != tip.init_bin_addr:
      print("init.bin addr mismatch. Expected {}, found {}".format(tip.init_bin_addr, title_init_bin_addr))
      exit(1)

    # move cursor to first paragraph
    cur += 2
    paragraphs = tip.cnparagraphs if lang_to_merge == "cn" else tip.enparagraphs
    for p_i, paragraph in enumerate(paragraphs):
      tips_inittxt_lines[cur + 1] = paragraph + "\n"
      jp_line_split = tips_inittxt_lines[cur].rstrip().split(";", 3)
      tip.jpparagraphs.append(jp_line_split[3])
      cur += 2

  # Write modified lines
  with open(saveas, "w", encoding="utf-8-sig") as f_out:
    for l in tips_inittxt_lines:
      f_out.write(l)


if __name__ == '__main__':
  main()
