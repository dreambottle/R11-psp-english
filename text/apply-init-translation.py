#!/usr/bin/python3
# -*- coding: utf-8 -*-

# a slower version of extract-init-bin-tables, which searches the text
# references, instead of doing a table lookup.

import sys
import re

seg_table = [0x1140, 0xac98]
seg_text = [0xba68, 0x2c11a]

def main():

  if len(sys.argv) != 4:
    exit("Usage: %s translation.txt in.init out.init")

  txt     = sys.argv[1]
  bin_in  = sys.argv[2]
  bin_out = sys.argv[3]

  f_txt=open(txt   , "rb")
  f_bin=open(bin_in, "rb")
  txt_lines = f_txt.readlines()
  init_bytes = bytearray(f_bin.read())
  f_txt.close()
  f_bin.close()

  head = init_bytes[:seg_text[0]]
  mv = memoryview(head)
  head_int = mv.cast("I")
  body = bytearray()
  
  jp_pattern = re.compile(b"^;([\da-fA-F]*);([\d]*);(.*)$")
  dupestr = b";dupe:"
  i = 0
  pos = 0
  while i < len(txt_lines):
    ln = txt_lines[i]
    match = jp_pattern.match(ln)
    if match:
      i += 1
      ln2 = txt_lines[i] if (i < len(txt_lines)) else b""
      ln2 = ln2.rstrip(b'\r\n')
      table_off = int(match.group(1), 16)
      
      if (ln2.startswith(dupestr)):
        dupe_ref_bytes = ln2[len(dupestr):]
        dupe_ref = int(dupe_ref_bytes, 16)
        # Just reference the same string
        head_int[table_off // 4] = head_int[dupe_ref // 4]
      else:
        jp_string = match.group(3)
        en_string = ln2 if ln2 else jp_string

        head_int[table_off // 4] = pos + seg_text[0]
        body += en_string + b'\x00'
        pos += len(en_string) + 1
    i += 1
  
  mv.release()

  f_out=open(bin_out, "wb")
  f_out.write(head)
  f_out.write(body)
  f_out.close()


if __name__ == '__main__':
  main();
