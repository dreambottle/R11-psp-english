#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

elf_head_size = 0xA0

text_area     = [0x12116c, 0x128710]
text_tables   = [0x12bb8c, 0x136aa0]

# text_s0_area  = [0x12116c, 0x1217d0]
# text_s0_table = [0x12bb8c, 0x123fb0]

# text_s1_area  = [0x1219c0, 0x123914]
# text_s1_table = [0x12bb8c, 0x123fb0]

# text_s2_area  = [0x12483c, 0x128620]
# text_s2_table = [0x136760, 0x136aa0]

relocation_area = [0x137528, 0x141520]
reloc_pos = relocation_area[0]

# def find_and_replace_addr(bytearr, limits, pos, new_pos):
#   if (limits):
#     bytearr = bytearr[limits[0]:limits[1]]
#   mv = memoryview(bytearr)
#   intlist = mv.cast("I")
#   found = False
#   print("Searching...")
#   for i in range(len(intlist)):
#     if intlist[i] == (pos - elf_head_size):
#       found = True
#       intlist[i] = new_pos - elf_head_size
#       print("=== Changed %X to %X at %X" % (pos, new_pos, i*4+ \
#         (limits[0] if limits else 0)))
#   if not found:
#     print("Not found: %X"%pos)
#   mv.release()


def patch(bytearr, initial_text, new_text, max_size, last_pos):
  global reloc_pos
  relocate = False
  if len(new_text)+1 > max_size:
    print("{0}/{1} length in '{2}'.".format(len(new_text)+1, max_size, new_text))
    relocate = True

  pos = bytearr.find(initial_text + b'\x00', last_pos, text_area[1])
  if pos == -1:
    print("NOT FOUND: {0}".format(new_text))
    return pos

  if relocate:
    pass
    #nope, does not work just yet
    # print(new_text)
    # print("Will be relocated to %X. (Not very safe, try to avoid this)" % reloc_pos)
    # bytearr[pos:pos+max_size] = b'\x00'*max_size

    # find_and_replace_addr(bytearr, text_tables, pos, reloc_pos)

    # new_size = (len(new_text)+1) | 0x3
    # new_text = new_text.ljust(new_size, b'\x00')
    # bytearr[reloc_pos:reloc_pos+new_size] = new_text

    # reloc_pos += new_size
  else:
    new_text = new_text.ljust(max_size, b'\x00')
    bytearr[pos:pos+max_size] = new_text
  return pos


def main():
  # Warning: can only work a clean BOOT.BIN

  if len(sys.argv) != 4:
    exit("Usage: %s translation.txt source-BOOT.BIN output-BOOT.BIN")

  txt     = sys.argv[1]
  bin_in  = sys.argv[2]
  bin_out = sys.argv[3]

  f_txt=open(txt, "rb")
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
  last_pos = text_area[0]
  for i, ln in enumerate(txt_lines):
    # print(i)
    ln = ln[:-1]
    if (state == JA):
      m = jp_pattern.match(ln)
      if (m):
        # off  = int(m.group(1), 16)
        size = int(m.group(2), 10)
        jap_text = m.group(3).strip(b'\r\n')
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
      res = patch(bin_bytes, jap_text, en_text, size, last_pos)
      if res != -1: pos = res
      else:
        exit("Cannot complete")

  
  f_bin=open(bin_out, "wb")
  f_bin.write(bin_bytes)
  f_bin.close()


if __name__ == '__main__':
  main();
