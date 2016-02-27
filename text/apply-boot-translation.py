#!/usr/bin/python3
# -*- coding: utf-8 -*-

# a slower version of extract-init-bin-tables, which searches the text
# references, instead of doing a table lookup.

import sys
import re

elf_head_size = 0xA0

text_area     = [0x12116c, 0x128710]
text_tables   = [0x12bb8c, 0x136aa0]

text_s0_area  = [0x12116c, 0x1217d0]
text_s0_table = [0x12bb8c, 0x123fb0]

text_s1_area  = [0x1219c0, 0x123914]
text_s1_table = [0x12bb8c, 0x123fb0]

text_s2_area  = [0x12483c, 0x128620]
text_s2_table = [0x136760, 0x136aa0]



def patch(bytelist, initial_text, new_text, max_size):
  if len(new_text)+1 > max_size:
    print("{0}/{1} length in '{2}'.".format(len(new_text)+1, max_size, new_text))
    # TODO: relocation
    print("Will be skipped.")
    return
  pos = bytelist.find(initial_text, text_area[0], text_area[1])
  print("%x"%pos, "%x"%(pos+max_size))
  if pos == -1:
    print ("'{0}' not found".format(new_text))
    return

  new_text = new_text.ljust(max_size, b'\x00')
  bytelist[pos:pos+max_size] = new_text

def main():
  # Warning: can only work a clean BOOT.BIN

  if len(sys.argv) != 4:
    exit("Usage: %s translation.txt source-BOOT.BIN output-BOOT.BIN")

  txt     = sys.argv[1]
  bin_in  = sys.argv[2]
  bin_out = sys.argv[3]

  f_txt=open(txt   , "rb")
  f_bin=open(bin_in, "r+b")

  txt_lines = f_txt.readlines()
  f_txt.close()
  bin_bytes = bytearray(f_bin.read())
  f_bin.close()

  jp_pattern = re.compile(b"^;([\da-fA-F]*);([\d]*);(.*)$")
  JA=1
  EN=2
  state=JA
  off  = None
  size = None
  jap_text = None
  en_text  = None
  for i, ln in enumerate(txt_lines):
    # print(i)
    ln = ln[:-1]
    if (state == JA):
      m = jp_pattern.match(ln)
      if (m):
        # off  = int(m.group(1), 16)
        size = int(m.group(2), 10)
        jap_text = m.group(3)
        # print("matched", size, jap_text)
        state = EN
        continue
      else:
        continue
    elif (state == EN):
      if ln.startswith(b"#"):
        continue

      state = JA
      if ln == b"":
        continue
      en_text = ln
      # print(jap_text, en_text, size)
      patch(bin_bytes, jap_text, en_text, size)

  
  f_bin=open(bin_out, "wb")
  f_bin.write(bin_bytes)
  f_bin.close()


if __name__ == '__main__':
  main();
