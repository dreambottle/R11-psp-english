#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script extracts translated lines for further text repackaging.
# Also: appends names, changes the encoding to sjis and replaces unsupported characters.

import argparse
import fileinput
import re
import sys
import os
import collections

import r11.names as names
import r11

debug = False
should_run_buffer_overflow_validations = False
validate_jp_text = True

STATE_BLANK = 0
STATE_JP = 1
STATE_TRANSLATED_EN = 2
STATE_TRANSLATED_CN = 3

class TlBucket:
  def __init__(self):
    self.jp = None
    self.en = None
    self.cn = None

tip_compiled_pattern = re.compile(r"(?:%TS([0-9]{3}))")

def detectTips(text: str) -> ():
  match = tip_compiled_pattern.search(text)
  return match.groups() if match else ()

def detectJpSpeakerAndBrackets(jp_line):
  # \u300c and \u300d are corner brackets: 「」, normally used for characters' direct speech
  # Note:
  # There are a few exceptions with corner bracket usage, like at line 1041 in CO4_02.txt,
  # where it is used not for direct speech, but as a regular quotation.
  
  #meta_pattern = r"(?:%[A-Zp][A-Z0-9]*)*?"
  main_text_pattern_ja = "^((?:[^%]*?\u300c)?).*?(\u300d)?$"
  match_ja = re.match(main_text_pattern_ja, jp_line)

  jp_speaker = match_ja.group(1) # always a speaker name + a corner bracket, or empty
  jp_trailing_bracket = match_ja.group(2)
  jp_leading_bracket = ""
  
  if debug: eprint("JP match %s,%s;"%(jp_speaker, jp_trailing_bracket))
  if debug and "\u300c" == jp_speaker:
    eprint("\u300c without a speaker %s %s,%s; %s"%(sys.argv[1], jp_speaker, jp_trailing_bracket, jp_line))

  if jp_speaker:
    jp_leading_bracket = jp_speaker[-1:]
    jp_speaker = jp_speaker[:-1] # crop bracket \u300c
  else:
    jp_speaker = ""

  return [jp_speaker, jp_leading_bracket, jp_trailing_bracket]

def loadJpMacChapterFile(chapter_name: str) -> [str]:
  orig_chapter_path = os.path.dirname(__file__) + "/../text/tmp/mac-ja-psp/" + chapter_name + ".txt"
  with open(orig_chapter_path, "r", encoding=r11.sjis_enc) as r11_jp_textfile:
    return r11_jp_textfile.readlines()
  
def filterTrueJpLines(lines: [str]) -> [str]:
  # starting from 4th line, every 2nd out of 3
  lines_filtered = [l.rstrip() for i, l in enumerate(lines[3:]) if i%3==1]
  return list(lines_filtered)

# parses lines from a chapters-psp/ file into a list of TlBucket objects
def loadTlBuckets(lines):
  state = STATE_JP
  tl_buckets = []
  current_tl_bucket = None

  tl_skip_lines = set([
    "%N%N%N%N",
    "%CF66A%FS%LCThis⑳story⑳has⑳not⑳finished⑳yet.%FE%N",
    "%C88FC%FS%LCThis⑳story⑳has⑳not⑳finished⑳yet.%FE%N",
    "%FS%LCThis⑳story⑳has⑳not⑳finished⑳yet.%FE%N",
    "%FS%LCTruth⑳is⑳not⑳revealed.%FE%N",
    "%FS%LCAnd⑳it⑳circulates⑳through⑳an⑳incident.%FE%N",
    "%FS%LC――⑳It⑳is⑳an⑳infinity⑳loop!%FE",
    "%O",
  ])

  for line in lines:
    line = line.rstrip("\n")
    if state == STATE_JP:
      if (line.strip() == ""):
        continue

      if (should_run_buffer_overflow_validations and "%K%P" in line and not line.endswith("%K%P")):
        eprint("Possible typo: found a symbol after '%%K%%P' in '%s'"%(line))
      
      current_tl_bucket = TlBucket()
      current_tl_bucket.jp = line
      tl_buckets.append(current_tl_bucket)
      state = STATE_TRANSLATED_EN
      
      # skips lines in tl_skip_lines
      # skips "-------------------------------------------" lines 
      # skips textless %N %O %P %p sequences
      if(line.strip() in tl_skip_lines) or \
          re.match(r"^(%[NOPp])+$", line) or \
          re.match(r"^(%FS)?-{40,}[%A-Z0-9]+$", line):
        state = STATE_JP
        if should_run_buffer_overflow_validations and ("%P" in line or "%O" in line): page_buf = 0
    
    elif state == STATE_TRANSLATED_EN:
      current_tl_bucket.en = line
      # look for CN line next
      state = STATE_TRANSLATED_CN
      if line.strip() == "":
        eprint("EN line was empty! (jp)'{}' [{}]".format(current_tl_bucket.jp, fileinput.filename()))
      
    elif state == STATE_TRANSLATED_CN:
      current_tl_bucket.cn = line
      if line.strip() == "":
        eprint("CN line was empty! (jp)'{}' [{}]".format(current_tl_bucket.jp, fileinput.filename()))
      # we have all lines, start looking for a JP line again
      state = STATE_JP
  #/for
  return tl_buckets

def prepareTlLines(tl_buckets, tl_suffix, current_filename, jp_mac_chapter_lines = None) -> bytes:
  out_lines_of_bytes_tl = []

  page_buf = 0

  # used to validate that jp lines have a 100% match with the original.
  jp_true_lines = filterTrueJpLines(jp_mac_chapter_lines) if jp_mac_chapter_lines else None


  for i, tlb in enumerate(tl_buckets):
    jp_line = tlb.jp
    en_line = tlb.en
    cn_line = tlb.cn

    jp_line = r11.clean_translation_enc_issues(jp_line)
    if jp_true_lines:
      jp_true_line = jp_true_lines[i]
      if jp_true_line != jp_line:
        eprint("JP source mismatch; expected:'{}'; was:'{}' (~{})[{}]".format(jp_true_line, jp_line, i*4, current_filename))
        jp_line = jp_true_line

    jp_trailing_meta = r11.find_trailing_control_sequence(jp_line)
    jp_tips = detectTips(jp_line)
    
    if (tl_suffix == "en" and not en_line):
      # output slightly cleaned up original if there's no TL
      en_line = r11.clean_en_translation_line(jp_line)
      out_lines_of_bytes_tl.append(r11.str_to_r11_bytes(jp_line, "en", exception_on_unknown=True) + b"\n")
      continue
    if (tl_suffix == "cn" and not cn_line):
      # output original if there's no TL
      out_lines_of_bytes_tl.append(r11.str_to_r11_bytes(jp_line, "cn", exception_on_unknown=True) + b"\n")
      continue

    jp_line = r11.rm_trailing_control_sequence(jp_line)
    [jp_speaker, jp_leading_bracket, jp_trailing_bracket] = detectJpSpeakerAndBrackets(jp_line)

    export_translated_line = ""
    trailing_meta = ""

    if tl_suffix == "en":
      en_trailing_meta = r11.find_trailing_control_sequence(en_line)
      en_tips = detectTips(en_line)
      if (jp_tips != en_tips):
        eprint("Tips tag missing. EN: {} JP: {}; (en)'{}' (~{})[{}]".format(en_tips, jp_tips, en_line, i*4, current_filename))
      en_line = r11.rm_trailing_control_sequence(en_line)
      en_line = r11.clean_en_translation_line(en_line)

      # nonen = re.findall(r"[^A-Za-z0-9!.,:;/?%\s〜―\"-*-「」♪『』α=！]", en_line)
      # nonenlen = len(nonen)
      # lineLen = len(en_line)
      # if nonenlen > 1:
      #   print("Warning! Found too many non-en chars: [{}] in line {}".format(nonen, en_line))
      
      if jp_speaker:
        translated_speaker = names.translateNamesString(jp_speaker, tl_suffix)
        # append TL'ed speaker + opening bracket
        export_translated_line = "{}{}".format(translated_speaker, jp_leading_bracket)
        if (jp_trailing_bracket != "\u300d"):
          raise Exception("Unexpected trailing bracket '{}' captured '{}' (~{})[{}]".format(jp_trailing_bracket, jp_line, i*4, current_filename))
      else:
        if (jp_trailing_bracket == "\u300d"):
          # Speaker was empty, but trailing bracket exists.
          if en_line.__contains__("\u300c"):
            # TL line has its own bracket. Won't append any more
            jp_trailing_bracket = ""
          else:
            # TL line has no bracket.
            # Will append opening bracket, trailing bracket will be appended later
            #TODO reformat text to get rid of this case
            export_translated_line = "\u300c"
            eprint("TL Line auto-bracketed 「」 '{}' (~{})[{}]".format(en_line, i*4, current_filename))

      export_translated_line += en_line
      export_translated_line += jp_trailing_bracket if jp_trailing_bracket else ""
      trailing_meta = en_trailing_meta if en_trailing_meta else jp_trailing_meta
    
    elif tl_suffix == 'cn':
      cn_trailing_meta = r11.find_trailing_control_sequence(cn_line)
      cn_tips = detectTips(cn_line)
      if (jp_tips != cn_tips):
        eprint("Tips tag missing. CN: {} JP: {}; (cn)'{}' (~{})[{}]".format(cn_tips, jp_tips, cn_line, i*4, current_filename))
      cn_line = r11.rm_trailing_control_sequence(cn_line)
      cn_line = r11.clean_cn_translation_line(cn_line)

      translated_speaker = names.translateNamesString(jp_speaker, tl_suffix)
      if not cn_line.startswith(translated_speaker):
        eprint("Speaker mismatch, expected {} at CN line '{}' (~{})[{}]".format(translated_speaker, cn_line, i*4, current_filename))
      export_translated_line = cn_line
      trailing_meta = cn_trailing_meta if cn_trailing_meta else jp_trailing_meta

    if should_run_buffer_overflow_validations:
      # check for buffer overflow. the game will probably run out of space on screen
      # before this, but that's harder to check given a variable width font.
      page_buf += len(export_translated_line)

      # Standard psp engine limit is 480
      if page_buf > 480:
        eprint("TEXT BUFFER OVERFLOW DETECTED. Predicted buffer size: %s at line #%s"%(page_buf, i))
      # if ja_speaker and len(export_translated_line) > 120:
      #   eprint("Warn: Single line size: %s at line #%s: %s"%(len(export_translated_line), i, export_translated_line))
      if ("%P" in trailing_meta or "%O" in trailing_meta):
        page_buf = 0

    export_translated_line += trailing_meta

    out_lines_of_bytes_tl.append(r11.str_to_r11_bytes(export_translated_line, lang=tl_suffix, exception_on_unknown=True) + b"\n")
  # end of for i, tlb in enumerate(tl_buckets):

  return out_lines_of_bytes_tl

def main():

  parser = argparse.ArgumentParser(description="This script extracts translated lines for further text repackaging." +
            " Also appends names, changes the encoding to sjis and replaces unsupported characters.")
  parser.add_argument('--input', '-i', type=str, help='input file')
  parser.add_argument('--output', '-o', type=str, help='output file')
  parser.add_argument('--tl', '-t', type=str, help="what translation to use. Provide 'en' or 'cn'", choices=['en', 'cn'])
  parser.add_argument('--onlytl', action='store_const', const=True, default=False, help="If specified, will only output translated lines.")

  args = parser.parse_args()

  assert args.input
  assert args.output
  assert args.tl
  assert args.onlytl != None

  lines = r11.readlines_utf8_crop_crlf(args.input)
  lines = [line for line in lines if not line.startswith("//")]
  tl_buckets = loadTlBuckets(lines)
  input_filename = os.path.basename(args.input)

  chaptername = input_filename[:-4]
  jp_mac_chapter_lines = loadJpMacChapterFile(chaptername) if not args.onlytl else None

  lines_tl = prepareTlLines(tl_buckets, args.tl, input_filename, jp_mac_chapter_lines)

  if (args.output):
    # tmp
    # hack_cn_utf8_dump = os.path.dirname(__file__) + "/../text/tmp/mac-cn-utf8/" + chaptername + ".txt"
    # hack_cn_utf8_full_dump = os.path.dirname(__file__) + "/../text/tmp/cn-text-utf8/fullscript.txt"
    # cn_full = open(hack_cn_utf8_full_dump, mode="a+", encoding="utf-8-sig")
    # cn_full.write(cn_line)
    
    # eprint("Writing preproc output to " + args.output + ". OnlyTL: " + str(args.onlytl))
    with open(args.output, "wb") as f:
      if (args.onlytl):
        f.writelines(lines_tl)
      
      else:
        # write first 3 lines as is
        f.writelines([r11.str_to_r11_bytes(l) for l in jp_mac_chapter_lines[:3]])

        # Then replace empty lines (every 3rd) with the translations
        for i, line_tl in enumerate(lines_tl):
          l = i * 3 + 3
          
          line_addr = r11.str_to_r11_bytes(jp_mac_chapter_lines[l], "en", exception_on_unknown=True)
          line_jp = r11.str_to_r11_bytes(jp_mac_chapter_lines[l+1], "en", exception_on_unknown=True)
          # to_write = [line_addr, line_jp, line_tl]
          f.write(line_addr)
          f.write(line_jp)
          f.write(line_tl)


def eprint(*args, **kwargs):
  print(*args, **kwargs, file=sys.stderr)

if __name__ == '__main__':
  main()
