#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import struct

# elf_head_size = 0xA0

# def find_in_table(table, value, table_position = 0):
#   #entries = len(table) // 4
#   #int_table = struct.unpack("<"+"I"*entries, table)
#   int_table = memoryview(table).cast("I");
#   offsets = [i*4+table_position for i, v in enumerate(int_table) if v == value]

#   if (len(offsets) == 0):
#     print("%x"%value, "not found")
 
#   if (len(offsets) > 1):
#     print("warn: found %d table offsets for %x:" % (len(offsets), value+elf_head_size))
#     for off in offsets:
#       print("- %x"%off)

#   return offsets


# def find_all_str_off(bytelist, table_section, text_section):
#   table = bytelist[table_section[0]:table_section[1]]

#   strings = []
#   lengths = []
#   table_offs = []

#   pos = text_section[0]
#   while pos < text_section[1]:
#     # print( "%x/%x" % (pos, len(bytelist)) )
#     table_off = find_in_table(table, pos-elf_head_size, table_section[0])
#     end = bytelist.find(b"\x00", pos)
#     # print("%x at %x"%(end, table_off))
#     if (end == -1): break
#     if (table_off):
#       strings.append(bytelist[pos:end])
#       lengths.append((end|3)-pos)
#       table_offs.append(table_off)
#       pos = end
    
#     pos = (pos + 4) & ~3; #align to next 4


#   return (table_offs, lengths, strings)

def main():

  # data_section_off = 0x129f80
  # data_section_size = 0x1e014

  text = [0x12116c, 0x128710]
  text_tables = [0x12bb8c, 0x136aa0]

  text_s0       = [0x12116c, 0x1217d0]
  text_s0_table = [0x12bb8c, 0x123fb0]
  
  text_s1       = [0x1219c0, 0x123914]
  text_s1_table = [0x12bb8c, 0x123fb0]

  text_s2       = [0x12483c, 0x128620]
  text_s2_table = [0x136760, 0x136aa0]

  path = sys.argv[1] if len(sys.argv) > 1 else "BOOT.BIN"
  outpath = path + ".jp.txt"

  f=open(path, "rb")
  # f.seek(data_section_off)
  data_bytes = f.read()
  f.close()

  f = open(outpath, "wb")

  strings0 = data_bytes[text_s0[0]:text_s0[1]].split(b'\x00')
  strings1 = data_bytes[text_s1[0]:text_s1[1]].split(b'\x00')
  strings2 = data_bytes[text_s2[0]:text_s2[1]].split(b'\x00')
  for s in strings0 + strings1 + strings2:
    if s != b'':
      f.write(b';;' + b"%d"%(len(s)|3,) + b';' + s + b'\n\n')
  f.close()
  # strings = find_all_str_off(data_bytes, text_tables, text)
  # strings = find_all_str_off(data_bytes, text_s2_table, text_s2)

  # for tup in strings:
  #   f.write(b";%x;%d;%s\n\n"%tup)
  # f.close()



if __name__ == '__main__':
  main();
