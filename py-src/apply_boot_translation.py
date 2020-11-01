#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

import r11

elf_head_size = 0xA0

text_area     = [0x12116c, 0x128698]
# text_tables   = [0x12bb8c, 0x136aa0]



def patch_find_and_replace(bytearr, original_text, new_text, max_len, find_from_pos, new_text_lang = "en"):

  original_bytes = r11.str_to_r11_bytes(original_text, exception_on_unknown=True) + b'\x00'
  
  if len(original_bytes)-1 > max_len:
    print("String buffer overflow. {0}/{1} '{2}'.".format(len(original_bytes)-1, max_len, new_text))
    raise Exception

  pos = bytearr.find(original_bytes, find_from_pos, text_area[1])
  if pos == -1:
    print("NOT FOUND: {} (TL: {})".format(original_text, new_text))
    return pos

  patch_pos(bytearr, pos, new_text, max_len, new_text_lang)
  return pos

def patch_pos(bytearr, pos, new_text, max_len, new_text_lang = "en"):
  text_bytes = r11.str_to_r11_bytes(new_text, new_text_lang, exception_on_unknown=True)

  # max_len specified in the txt file does not include a 0x00-byte terminator
  if (len(text_bytes) > max_len):
    cut = text_bytes[:max_len]
    print("Cutting line", new_text, "->", cut)
    text_bytes = cut

  # final 0-byte, also filling any remaining space with 0
  text_bytes = text_bytes.ljust(max_len+1, b'\x00')
  bytearr[pos:pos+max_len+1] = text_bytes

def main():
  # Warning: only works on a clean BOOT.BIN

  if len(sys.argv) != 5:
    exit("Usage: %s translation.txt source-BOOT.BIN output-BOOT.BIN en|cn")
  
  print("Applying BOOT.BIN translation.")

  txt     = sys.argv[1]
  bin_in  = sys.argv[2]
  bin_out = sys.argv[3]
  lang    = sys.argv[4]

  print("Using encoding table lang: {}".format(lang))

  f_bin=open(bin_in, "r+b")
  bin_bytes = bytearray(f_bin.read())
  f_bin.close()

  txt_lines = r11.readlines_utf8_crop_crlf(txt)
  txt_lines = [t for t in txt_lines if not t.startswith("#")]

  jp_pattern = re.compile("^;([\da-fA-F]*);([\d]*);(.*)$")
  JP=1
  TL=2
  state=JP

  off  = None
  size = None
  jap_text = None
  tl_text  = None
  last_pos = text_area[0]
  for i, ln in enumerate(txt_lines):
    # print(i)
    # ln = ln[:-1]
    if (state == JP):
      m = jp_pattern.match(ln)
      if (m):
        offstr = m.group(1)
        off  = int(offstr, 16) if len(offstr)>0 else None
        size = int(m.group(2), 10)
        jap_text = m.group(3)

        if (ln.startswith("メモリースティック™に保存したデータ")):
          print(ln)
          print(jap_text)
        state = TL
        continue
      else:
        continue
    elif (state == TL):
      state = JP
      if ln == "":
        continue
      tl_text = ln
      # print(jap_text, en_text, size)
      if (off != None):
        patch_pos(bin_bytes, off, tl_text, size, lang)
        last_pos = off
      else:
        res = patch_find_and_replace(bin_bytes, jap_text, tl_text, size, last_pos, lang)
        if res != -1: last_pos = res
        else:
          raise Exception("Cannot complete")

  
  f_bin=open(bin_out, "wb")
  f_bin.write(bin_bytes)
  f_bin.close()
  print("BOOT text replaced.")


if __name__ == '__main__':
  main();
