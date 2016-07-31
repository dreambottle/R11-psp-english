#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# a slower version of extract-init-bin-tables, which searches the text
# references, instead of doing a table lookup.

import sys
import re

# Layout:
# 0x0 8 bytes - magic header (09 11 00 60 08 00 00 00)
# 0x8 - shortcut data offset (default: 0xf30)
# 0xc - table offset (value: 0x10)
# 0x10 30 * 0x34 byte blocks - table
# In each block:
#   0x0 - (u32) title text offset
#   0x4 - (u32) description text offset
#   0x8 - (u32) shortcut data offset
#   0xc-0x2f - ?????
#   0x30 - (u32) 0
# 06f8 - 0 marks end of the table
# 0x6fc - Texts
# 0xf30 - shortcut data (align: 4 bytes)
# 0x36c8 - ???? magic data with a table with shortcut data offsets
#           table starts at 0x30, every 2nd int32, count: 90 (0x5a)
table_offset = 0x10
table_entry_sz = 0x34
table_entry_count = 30
text = [0x62c, 0xf2e]
shortcut_data_offset = 0xf30
data2_offset = 0x36c8
data2_table_off = 0x30
data2_table_sz = 90

def main():

  if len(sys.argv) != 4:
    exit("Usage: %s translation.txt in.SHORTCUTS.SCN out.SHORTCUTS.SCN"%(sys.argv[0]))

  txt     = sys.argv[1]
  bin_in  = sys.argv[2]
  bin_out = sys.argv[3]

  f_txt=open(txt   , "rb")
  f_scn=open(bin_in, "rb")

  txt_lines = f_txt.readlines()
  f_txt.close()
  scn_bytes = bytearray(f_scn.read())
  f_scn.close()

  head = scn_bytes[:text[0]]
  text_magic_tail = scn_bytes[text[1]:text[1]+2] # not sure if it is important or not
  shortcut_data = scn_bytes[shortcut_data_offset:data2_offset]
  data2 = scn_bytes[data2_offset:]

  head_mv = memoryview(head)
  head_int = head_mv.cast("I")
  data2_mv = memoryview(data2)
  data2_int = data2_mv.cast("I")

  body = bytearray()
  
  jp_pattern = re.compile(b"^;([\da-fA-F]*);([\d]*);(.*)$")
  text_pos = 0
  for ln in txt_lines:
    match = jp_pattern.match(ln)
    if match:
      table_off = int(match.group(1), 16)
      string = match.group(3)
      size = len(string)

      head_int[table_off // 4] = text_pos + text[0]
      body += string + b'\x00'
      text_pos += size + 1
  
  # adjust data offsets
  # new_data_offset = ((text[0]+text_pos) & ~0xf) + 0x10  # align new offset
  new_data_offset = shortcut_data_offset # Keep old offset. Least buggy, but the texts must fit.
  data_offset_diff = new_data_offset - shortcut_data_offset
  print("Shortcuts data offset", new_data_offset, data_offset_diff)

  if (data_offset_diff != 0):
    #TODO
    head_int[2] = new_data_offset

    for i in range(table_entry_count):
      data_offset_i = (table_offset + i*table_entry_sz + 0x8) // 4
      head_int[data_offset_i] += data_offset_diff

    # data2
    for i in range(data2_table_sz):
      data2_int[data2_table_off//4 + 1 + i*2] += data_offset_diff

  head_mv.release()
  data2_mv.release()

  f_out=open(bin_out, "wb")
  f_out.write(head)
  f_out.write(body)
  # f_out.write(text_magic_tail)
  f_out.seek(new_data_offset)
  f_out.write(shortcut_data)
  f_out.write(data2)
  f_out.close()


if __name__ == '__main__':
  main();
