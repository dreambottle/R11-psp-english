#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script extracts translated lines for further text repackaging.
# Also: appends names, changes the encoding to sjis and replaces unsupported characters.

from names import names
import fileinput
import re
import sys

debug = False
text_validations = True

STATE_BLANK = 0
STATE_JA = 1
STATE_TRANSLATED = 2

def main():
  state = STATE_JA
  i = 0
  last_ja_line = ""

  page_buf = 0

  for line in fileinput.input():
    i += 1
    line = line.rstrip()

    if (re.search("^\s*//", line)):
      if debug: eprint("skipping comment {}:{}".format(i, line))
      continue

    if state == STATE_JA:
      if (line == ""):
        continue

      if (text_validations and "%K%P" in line and not line.endswith("%K%P")):
        eprint("Possible typo: symbol after '%%K%%P' in line#%s: %s"%(i, line))
      
      last_ja_line = line
      state = STATE_TRANSLATED

      # ⑳ ('CIRCLED NUMBER TWENTY' (U+2473)) found in "It's an infinity loop" text blocks
      if("\u2473" in line) or \
          re.match(r"^(%[NOPp])+$", line) or \
          re.match(r"^(%FS)?-{40,}[%A-Z0-9]+$", line):
        line = re.sub("\u2473", "  ", line)
        # just keep these as is
        state = STATE_JA
        if text_validations and ("%P" in line or "%O" in line): page_buf = 0
        println_sjis(line)

    elif state == STATE_TRANSLATED:
      translated_trailing_meta = re.search(r"\s*((?:%[KNOP])+)$", line)
      translated_trailing_meta = translated_trailing_meta.group(0) if translated_trailing_meta else "" # now its a string
      # if translated_trailing_meta: eprint("translated_trailing_meta %s" % translated_trailing_meta)

      # TODO make this reusable in TIPS
      line = re.sub(r"\s*((?:%[KNOP])+)$", "", line) # override the original escape codes if the translation specifies some
      line = re.sub(r"%(?![A-Z])", "\uff05", line) # replacing % metachar, with a lookalike char
      line = re.sub("\uff5e", "\u301c", line) # two versions of tilde, only one of which has a shift_jis codepoint
      line = re.sub("\u2013|\u2014", "\u2015", line) # likewise for mdash '―'
      line = re.sub("\u2015\u2015", "\u2015", line) # double -> single emdash
      line = re.sub("\uff0d", "-", line) # fullwidth minus hyphen -> '-'
      # ($en_linebreak || $p) =~ /%K$/ and $_ .= " "; # no trailing newline, so the sentence will be continued
      line = re.sub(r"(?<!\b\S \S)  +", " ", line) # collapse multiple spaces unless there are also extra spaces within the neighboring words
      line = re.sub("\u00f6", "o", line) # ö no shift_jis for vowel+macron. which is strange considering that it's used by Hepburn
      line = re.sub("\u014d", "o", line) # no shift_jis for vowel+macron. which is strange considering that it's used by Hepburn
      line = re.sub("\u00e9", "e", line) # é (utf8:c3a9) in fiancé; SA5_07, TIP_102
      line = re.sub("na\u00efve", "naive", line) # "naïve": no umlaut for i
      line = re.sub(r"''I''", "%CFF8FI%CFFFF", line) # colored text (yellow) to signify "ore", as deviated from Kokoro's normal "watashi".
      line = re.sub(r"'I'", "%C8CFFI%CFFFF", line) # colored text (blue) to signify "watashi", as deviated from Satoru's normal "ore".
      if "''" in line:
        exit("unmatched ''")
      # line = re.sub("\u2473", "\u2473", line) # ⑳ ('CIRCLED NUMBER TWENTY' (U+2473)). No need to replace, rendered as a wide space. (glyph #1147)
      # spaces are too thin on pc; Not the case for psp.
      
      last_ja_line = re.sub(r"%TS\d+|%TE", "", last_ja_line) # remove ja tips. any that make sense will be in the translation.
      
      # split ja line

      # \u300c and \u300d are corner brackets: 「」, normally used for characters' direct speech
      # Note:
      # There are a few exceptions with corner bracket usage, like at line 1041 in CO4_02.txt,
      # where it is used not for direct speech, but as a regular quotation.
      
      meta_pattern = "(?:%[A-Zp][A-Z0-9]*)*"
      main_text_pattern_ja = "^({0})((?:.+?\u300c)?).*?(\u300d)?({0})$".format(meta_pattern)
      match_ja = re.match(main_text_pattern_ja, last_ja_line)
      
      leading_meta = match_ja.group(1)
      ja_speaker = match_ja.group(2) # always a speaker name + a corner bracket, or empty
      ja_trailing_bracket = match_ja.group(3)
      ja_trailing_meta = match_ja.group(4)

      if debug: eprint("JA match %s:%s,%s,%s,%s;"%(i, leading_meta, ja_speaker, ja_trailing_bracket, ja_trailing_meta))

      if (leading_meta and ja_speaker):
        exit("Leading meta in combination w/ speaker exists! %s: %s"%(i, leading_meta))
      
      export_translated_line = leading_meta

      if (ja_speaker):
        ja_speaker = ja_speaker[:-1] # crop bracket \u300c
        # \u30fb (middle dot: ・) is used to separate multiple speakers in JA text
        translated_names_list = [names.get(s) for s in ja_speaker.split("\u30fb")]
        if (None in translated_names_list):
          exit("Speaker translation for %s not found. Values: %s"%(ja_speaker, translated_names_list))
        translated_speaker = ",".join(translated_names_list)
        export_translated_line = "{}{}\u300c".format(export_translated_line, translated_speaker)
        if (ja_trailing_bracket != "\u300d"):
          exit("Unexpected trailing bracket '%s' captured at line#%s: %s"%(ja_trailing_bracket, i, last_ja_line))
      else:
        # don't append trailing bracket
        ja_trailing_bracket = ""
      
      export_translated_line += line
      export_translated_line += ja_trailing_bracket if ja_trailing_bracket else ""

      trailing_meta = translated_trailing_meta if translated_trailing_meta else ja_trailing_meta

      if text_validations:
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

      println_sjis(export_translated_line)

      # state = STATE_BLANK
      state = STATE_JA

    # elif (state == STATE_BLANK):
    #   if (line != ""):
    #     exit("Blank line missing at line %d: %s"%(i, line));
    #   state = STATE_JA
  
  # re.purge()

def println_sjis(line):
  sys.stdout.buffer.write(line.encode("shift_jis_2004"))
  sys.stdout.buffer.write(b'\n')
  if debug: sys.stdout.buffer.flush()


def eprint(*args, **kwargs):
  print(*args, **kwargs, file=sys.stderr)

if __name__ == '__main__':
  main();