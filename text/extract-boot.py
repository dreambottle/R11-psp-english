#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import struct

def main():

  # text = [0x12116c, 0x128710]
  texts = [
    [0x12116c, 0x1217d0],
    [0x1219c0, 0x12465c],
    [0x12483c, 0x128620]
    ]

  path = sys.argv[1] if len(sys.argv) > 1 else "BOOT.BIN"
  outpath = path + ".jp.txt"

  f=open(path, "rb")
  data_bytes = f.read()
  f.close()

  f = open(outpath, "wb")

  strings = data_bytes[texts[0][0]:texts[0][1]].split(b'\x00')
  strings += data_bytes[texts[1][0]:texts[1][1]].split(b'\x00')
  strings += data_bytes[texts[2][0]:texts[2][1]].split(b'\x00')

  for s in strings:
    if s != b'':
      f.write(b';;' + str(len(s)|3).encode() + b';' + s + b'\n\n')
  f.close()


if __name__ == '__main__':
  main();
