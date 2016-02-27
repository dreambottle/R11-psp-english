#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import struct

def main():

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


if __name__ == '__main__':
  main();
