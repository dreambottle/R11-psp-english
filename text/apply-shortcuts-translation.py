#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# a slower version of extract-init-bin-tables, which searches the text
# references, instead of doing a table lookup.

import sys
import re

text_table = [0x0, 0x62c]
text = [0x62c, 0xf2e]

def main():

  if len(sys.argv) != 4:
    exit("Usage: %s translation.txt in.SHORTCUTS.SCN out.SHORTCUTS.SCN")

  txt     = sys.argv[1]
  bin_in  = sys.argv[2]
  bin_out = sys.argv[3]

  f_txt=open(txt   , "rb")
  f_scn=open(bin_in, "rb")

  txt_lines = f_txt.readlines()
  f_txt.close()
  scn_bytes = bytearray(f_scn.read())
  f_scn.close()

  head = scn_bytes[text_table[0]:text_table[1]]
  tail = scn_bytes[text[1]:]

  mv = memoryview(head)
  head_int = mv.cast("I")

  body = bytearray()
  
  jp_pattern = re.compile(b"^;([\da-fA-F]*);([\d]*);(.*)$")
  pos = 0
  for ln in txt_lines:
    match = jp_pattern.match(ln)
    if match:
      table_off = int(match.group(1), 16)
      string = match.group(3)
      size = len(string)

      head_int[table_off // 4] = pos + text[0]
      body += string + b'\x00'
      pos += size + 1
  
  mv.release()

  f_out=open(bin_out, "wb")
  f_out.write(head)
  f_out.write(body)
  f_out.write(tail)
  f_out.close()


if __name__ == '__main__':
  main();
