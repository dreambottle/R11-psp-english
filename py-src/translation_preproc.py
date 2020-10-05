#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script extracts translated lines for further text repackaging.
# Also: appends names, changes the encoding to sjis and replaces unsupported characters.

import fileinput
import re
import sys

from r11.names import names
import r11

debug = False
should_run_text_validations = True

STATE_BLANK = 0
STATE_JA = 1
STATE_TRANSLATED_EN = 2
STATE_TRANSLATED_CN = 3

def main():
  state = STATE_JA
  i = 0
  translatable_ja_line = ""

  page_buf = 0

  # for line in fileinput.input():
  #   i += 1
  #   line = line.rstrip()

  #   if (re.search(r"^\s*//", line)):
  #     if debug: eprint("skipping comment {}:{}".format(i, line))
  #     continue

  lines = [line.rstrip() for line in fileinput.input() if not line.startswith("//")]

  for line in lines:
    if state == STATE_JA:
      if (line == ""):
        continue

      if (should_run_text_validations and "%K%P" in line and not line.endswith("%K%P")):
        eprint("Possible typo: found a symbol after '%%K%%P' in line#%s: %s"%(i, line))
      
      translatable_ja_line = line
      state = STATE_TRANSLATED_EN

      # lines to copy as is when parsing a TL
      # ⑳ ('CIRCLED NUMBER TWENTY' (U+2473)) found in "It's an infinity loop" text blocks
      if("\u2473" in line) or \
          re.match(r"^(%[NOPp])+$", line) or \
          re.match(r"^(%FS)?-{40,}[%A-Z0-9]+$", line):
        # line = re.sub("\u2473", "  ", line)
        # just keep these as is
        r11.println_r11(r11.clean_en_translation_line(line))
        state = STATE_JA
        line = r11.clean_en_translation_line(line)
        if should_run_text_validations and ("%P" in line or "%O" in line): page_buf = 0

    elif state == STATE_TRANSLATED_EN:
      # TODO break this code down and simplify. No need to do everything when i'm first trying to break it into JP-EN-CN triplets.
      translated_trailing_meta = re.search(r"\s*((?:%[KNOP])+)$", line)
      translated_trailing_meta = translated_trailing_meta.group(0) if translated_trailing_meta else "" # now its a string
      # if translated_trailing_meta: eprint("translated_trailing_meta %s" % translated_trailing_meta)

      # TODO make this reusable in TIPS
      line = r11.rm_trailing_escape_codes(line)
      line = r11.clean_en_translation_line(line)
     
      translatable_ja_line = re.sub(r"%TS\d+|%TE", "", translatable_ja_line) # remove ja tips. any that make sense will be in the translation.
      
      # split ja line

      # \u300c and \u300d are corner brackets: 「」, normally used for characters' direct speech
      # Note:
      # There are a few exceptions with corner bracket usage, like at line 1041 in CO4_02.txt,
      # where it is used not for direct speech, but as a regular quotation.
      
      meta_pattern = "(?:%[A-Zp][A-Z0-9]*)*"
      main_text_pattern_ja = "^({0})((?:.*?\u300c)?).*?(\u300d)?({0})$".format(meta_pattern)
      match_ja = re.match(main_text_pattern_ja, translatable_ja_line)
      
      leading_meta = match_ja.group(1)
      ja_speaker = match_ja.group(2) # always a speaker name + a corner bracket, or empty
      ja_trailing_bracket = match_ja.group(3)
      ja_trailing_meta = match_ja.group(4)

      if debug: eprint("JA match %s:%s,%s,%s,%s;"%(i, leading_meta, ja_speaker, ja_trailing_bracket, ja_trailing_meta))

      if "\u300c" == ja_speaker:
        if debug: 
          eprint("\u300c without a speaker %s %s:%s,%s,%s,%s; %s"%(sys.argv[1], i, leading_meta, ja_speaker, ja_trailing_bracket, ja_trailing_meta, translatable_ja_line))
      elif (leading_meta and ja_speaker):
        exit("Leading meta in combination w/ speaker exists! %s: %s"%(i, leading_meta))
      
      export_translated_line = leading_meta

      if (ja_speaker):
        ja_speaker = ja_speaker[:-1] # crop bracket \u300c
        if ja_speaker:
          # \u30fb (middle dot: ・) is used to separate multiple speakers in JA text
          translated_names_list = [names.get(s) for s in ja_speaker.split("\u30fb")]
          if (None in translated_names_list):
            exit("Speaker translation for %s not found. Values: %s"%(ja_speaker, translated_names_list))
          translated_speaker = ",".join(translated_names_list)
          export_translated_line = "{}{}\u300c".format(export_translated_line, translated_speaker)
          if (ja_trailing_bracket != "\u300d"):
            exit("Unexpected trailing bracket '%s' captured at line#%s: %s"%(ja_trailing_bracket, i, translatable_ja_line))
        else:
          if (ja_trailing_bracket == "\u300d"):
            export_translated_line += "\u300c"
          else:
            # handle inside the text
            pass
      else:
        # don't append trailing bracket
        ja_trailing_bracket = ""
      
      export_translated_line += line
      export_translated_line += ja_trailing_bracket if ja_trailing_bracket else ""

      trailing_meta = translated_trailing_meta if translated_trailing_meta else ja_trailing_meta

      if should_run_text_validations:
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

      r11.println_sjis(export_translated_line)

      # look for CN line next
      state = STATE_TRANSLATED_CN
      
    elif state == STATE_TRANSLATED_CN:
      # TODO

      # we have all lines, start looking for a JP line again
      state = STATE_JA


def eprint(*args, **kwargs):
  print(*args, **kwargs, file=sys.stderr)

if __name__ == '__main__':
  main()
