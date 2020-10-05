#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Used to automatically import matching lines from tlwiki translations

import sys
import re

def find_en_match(line, fromm, pattern):
  match_iter = pattern.finditer(fromm)
  for match in match_iter:
    if match.group(1).encode("SJIS") == line:
      print(match.group(2))
      return match.group(2).encode("SJIS")
  return None

def get_dictionary(source_text, pattern):
  matches = pattern.finditer(source_text)
  matchdict = dict()
  for match in matches:
    # print(match.group(1), match.group(2))
    matchdict[match.group(1).encode("SJIS").strip()] = \
              match.group(2).encode("SJIS").strip()
  return matchdict

def main():
  if (len(sys.argv) != 3):
    exit("usage: {0} target.jp.txt source.en.txt".format(sys.argv[0]))
  
  target = sys.argv[1]
  source = sys.argv[2]

  f_target = open(target, "r+b")
  f_source = open(source, "r", encoding="UTF8")

  target_lines = [s.strip() for s in f_target.readlines()]
  source_text = f_source.read()

  result_lines = []

  jp_pattern = re.compile(b"^;([\da-fA-F]*);([\d]*);(.*)")
  # dupe_pattern = re.compile("^;dupe:([\da-zA-Z]+)")
  init_txt_pattern = re.compile("^#\[[x:,0-9]*]: '(.*?)'$\n(?:^#.*\n)?"
      "^\[[x:,0-9]*]: '(.*?)'$", re.M)


  current_dict = get_dictionary(source_text, init_txt_pattern)

  for i, t_line in enumerate(target_lines):
    t_line = t_line.strip()
    result_lines.append(t_line)
    
    jp_match = jp_pattern.match(t_line)
    if (jp_match and jp_match.group(3) != "" and \
          not target_lines[i+1].startswith(b";dupe:")):
      en_match = current_dict.pop(jp_match.group(3), None)
      if (en_match):
        result_lines.append(en_match)

  f_target = open("out.txt", "wb")
  for l in result_lines:
    f_target.write(l + b'\n')

  f_target.write(b"#====== Unmatched lines from " + source.encode('SJIS') + b'\n\n')
  for k, v in current_dict.items():
    f_target.write(k + b"\n" + v + b"\n\n")

  f_target.close()

if __name__ == '__main__':
  main()