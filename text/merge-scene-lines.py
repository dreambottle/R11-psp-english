#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

def main():
  if len(sys.argv) != 4:
    sys.exit("usage: %s jap.extracted.txt en.lines.txt out.combined.txt" % sys.argv[0])
  else:
    jap = sys.argv[1]
    en  = sys.argv[2]
    out = sys.argv[3]

  jap_f = open(jap, "rb")
  en_f  = open(en,  "rb")
  
  jap_lines = jap_f.readlines()
  en_lines  = en_f.readlines()

  jap_head = jap_lines[:3]
  jap_payload = jap_lines[3:]
  jap_entries_count = (len(jap_payload)) // 3
  
  if len(en_lines) != jap_entries_count:
    print("Entry count mismatch!", "Lines jap: %d(effective:%d), en: %d." % (len(jap_lines), jap_entries_count, len(en_lines)) )

  out_f = open(out, "wb")
  for i in range(len(jap_head)):
    out_f.write(jap_head[i])


  for i in range(len(en_lines)):
    if i < jap_entries_count:
      out_f.write(jap_payload[i*3])
      out_f.write(jap_payload[i*3+1])
    if i < len(en_lines):
      out_f.write(en_lines[i])
  out_f.close()
  jap_f.close()
  en_f.close()


if __name__ == '__main__':
  main()
