#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

import r11


table_offset = 0x10
table_entry_sz = 0x34
table_entry_count = 30
addr_text = [0x62c, 0xf2e]
shortcut_data_offset = 0xf30
data2_offset = 0x36c8
data2_table_off = 0x30
data2_table_sz = 90

def main():

  if not 4 <= len(sys.argv) <= 5:
    exit("Usage: %s translation.txt in.SHORTCUTS.SCN out.SHORTCUTS.SCN <(optional) translation_lang='en'>"%(sys.argv[0]))

  txt     = sys.argv[1]
  bin_in  = sys.argv[2]
  bin_out = sys.argv[3]
  encoding_table_lang = sys.argv[4] if sys.argv[4] else "en"

  txt_lines = r11.readlines_utf8_crop_crlf(txt)
  with open(bin_in, "rb") as f_scn:
    scn_bytes = bytearray(f_scn.read())

  
  head = scn_bytes[:addr_text[0]]
  # two bytes "0x90 0x90" not sure what they do. Could be just an alignment artifact
  text_magic_tail = scn_bytes[addr_text[1]:addr_text[1]+2]
  shortcut_data = scn_bytes[shortcut_data_offset:data2_offset]
  data2 = scn_bytes[data2_offset:]

  head_mv = memoryview(head)
  head_int = head_mv.cast("I")

  body = bytearray()
  
  jp_pattern = re.compile("^;([\da-fA-F]*);([\d]*);(.*)$")
  text_pos = 0
  text_max_len = 0
  for ln in txt_lines:
    match = jp_pattern.match(ln)
    if match:
      table_off = int(match.group(1), 16)
      max_len = int(match.group(2), 10)
      string = match.group(3)

      text_max_len += max_len + 1

      str_bytes = r11.str_to_r11_bytes(string, encoding_table_lang, exception_on_unknown=True)
      
      strbytelen = len(str_bytes) + 1
      body += str_bytes + b'\x00'

      head_int[table_off // 4] = addr_text[0] + text_pos
      text_pos += strbytelen
  
  print("text_max_len: {}".format(text_max_len))
  if (text_pos > text_max_len):
    raise Exception("(text_pos > text_max_len: {} > {}".format(text_pos, text_max_len))

  # adjust data offsets
  # new_data_offset = ((text[0]+text_pos) & ~0xf) + 0x10  # align new offset
  new_data_offset = shortcut_data_offset # Keep old offset. No bugs, but all texts must fit the original size.
  # data_offset_diff = new_data_offset - shortcut_data_offset
  # print("Shortcuts data offset", new_data_offset, data_offset_diff)
  # if (data_offset_diff != 0):
  #   head_int[2] = new_data_offset

  #   for i in range(table_entry_count):
  #     data_offset_i = (table_offset + i*table_entry_sz + 0x8) // 4
  #     head_int[data_offset_i] += data_offset_diff

  #   # data2
  #   data2_mv = memoryview(data2)
  #   data2_int = data2_mv.cast("I")
  #   for i in range(data2_table_sz):
  #     data2_int[data2_table_off//4 + 1 + i*2] += data_offset_diff

  # data2_mv.release()
  head_mv.release()

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
