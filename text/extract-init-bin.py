#!/usr/bin/python3
# -*- coding: utf-8 -*-

# a slower version of extract-init-bin-tables, which searches the text
# references, instead of doing a table lookup.

import sys
import struct

def find_table_offset(table, pos, start=0):
  # Aligning to 4
  start = (start >> 2) << 2
  offsets = []
  for i in range(start, len(table), 4):
    val=int.from_bytes(table[i:i+4], "little")
    if val == pos: offsets.append(i)

  if (len(offsets) == 0): return 0

  if (len(offsets) > 1):
    print("warn: found", len(offsets), "table offsets for" , pos, ":", offsets)
  return offsets[0]


def find_all_str_off(all_bytes, text_start, table_end):
  # text = all_bytes[text_start:]
  table = all_bytes[:table_end]
  pos = text_start
  strings = []
  offs = []
  table_offs = []

  while pos < len(all_bytes):
    # print( "%x/%x" % (pos, len(all_bytes)) )
    table_off = find_table_offset(table, pos)
    if (table_off):
      end = all_bytes.find(b"\x00", pos)
      # print("%x at %x"%(end, table_off))
      if (end == -1): break
      strings.append(all_bytes[pos:end])
      offs.append(pos)
      table_offs.append(table_off)
      pos = end
    
    pos += 1


  return (table_offs, offs, strings)

def main():

  initbin_path = sys.argv[1] if len(sys.argv) > 1 else "init.dec"
  txt_path = initbin_path + ".jp.txt"

  f=open(initbin_path, "r+b")
  all_bytes = f.read()
  f.close()

  lines = find_all_str_off(all_bytes, 0xba68, 0xac98)

  n = len(lines[0])
  print(n)
  f = open("all.init.bin.txt", "wb")
  f.write(b'#===all strings found in the table are listed here\n\n')
  for i in range(n):
    tos = (lines[0][i],
           lines[1][i],
           lines[2][i])
    f.write(b"#;%x;%x;%s\n\n\n" % tos)
  f.close()

  # f_out = open(txt_path, "wb")


if __name__ == '__main__':
  main();
