#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import mmap
import struct


def main():
  if len(sys.argv) != 4:
    sys.exit("usage: %s translated.txt oldscene.SCN out-newscene.SCN" % sys.argv[0]);
  else:
    txt = sys.argv[1];
    old = sys.argv[2];
    new = sys.argv[3];

    txt_f = open(txt, "rb");
    # old_f = ;

    txt_lines = txt_f.readlines();
    txt_f.close();

    text_area = {'offset': int(txt_lines[1], 16), 'size': int(txt_lines[2], 16)}
    # print(text_area);
    entries = txt_lines[3:];

    with open(old, "r+b") as old_f:
      old_mm = mmap.mmap(old_f.fileno(), 0);

      new_f = open(new, "wb");
      new_f.write(old_mm[:text_area['offset']]);

      int_struct = struct.Struct("I");

      for i in range(len(entries) // 3):
        reference_off = int(entries[i*3], 16);
        jap_line = entries[i*3+1].replace(b"\n", b"\x00");
        en_line  = entries[i*3+2].replace(b"\n", b"\x00");
        pos = new_f.tell();
        pos_bytes = int_struct.pack(pos);
        new_f.seek(reference_off);
        new_f.write(pos_bytes);
        new_f.seek(pos);
        new_f.write(en_line);
      new_f.write(old_mm[-24:]);
      new_f.close();
      old_mm.close();

      



if __name__ == '__main__':
  main();