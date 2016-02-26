#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Used to automatically import matching lines from tlwiki translations

import sys
import re

def main():
  if (len(sys.argv) != 3):
    exit("usage: {0} target.jp.txt source.en.txt".format(sys.argv[0]))
  
  target = sys.argv[1]
  source = sys.argv[2]

  f_target = open(target, "r+b")
  f_source = open(source, "r", encoding="UTF8")

  target_lines = f_target.readlines()
  source_lines = f_source.readlines()

  jp_pattern = re.compile(b"^;([\da-fA-F]*);([\d]*);(.*)")
  shortcut_pattern = re.compile("^[a-f0-9]+: (.*?)$")
  
  f_target.seek(0)
  f_target.truncate()
  for i in range(len(target_lines) // 2):
    jp_match = jp_pattern.match(target_lines[i*2])
    en_match = shortcut_pattern.match(source_lines[i*3+1])
    f_target.write(b"#" + target_lines[i*2])
    print(jp_match.group(1), jp_match.group(2), en_match.group(1))
    f_target.write(b";%b;%b;%b\n\n"%\
              (jp_match.group(1), jp_match.group(2), en_match.group(1).encode("SJIS")))

  f_target.close();

if __name__ == '__main__':
  main();