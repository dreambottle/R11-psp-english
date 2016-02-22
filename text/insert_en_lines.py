#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import re

def main():
  if len(sys.argv) != 4:
    sys.exit("usage: %s jap.extracted.txt en.lines.txt out.combined.txt" % sys.argv[0]);
  else:
    jap = sys.argv[1];
    en  = sys.argv[2];
    out = sys.argv[3];

  #, encoding="SHIFT-JIS"
  jap_f = open(jap, "rb");
  en_f  = open(en,  "rb");
  
  jap_lines = jap_f.readlines();
  en_lines  = en_f.readlines();

  jap_head = jap_lines[:3];
  jap_payload = jap_lines[3:];
  jap_entries_count = (len(jap_payload)) // 3;
  
  # Trying to fix some common stuff
  corrections = 0;
  for i in range(jap_entries_count):
    # print ("line", i*3+1+3)
    jap_line = jap_payload[i*3+1];
    
    # inserting missing newlines
    res = re.search(b"^(?:%N)+$", jap_line);
    if (res and (i < len(en_lines)) and (en_lines[i] != jap_line)):
      if (re.search(b"^(?:%N)+$", en_lines[i])):
        # wrong number of newlines
        # will be corrected by "endings" corrector
        # en_lines[i] = jap_line;
        pass
      else:
        # no newlines at all
        en_lines.insert(i, jap_line);
        corrections += 1;

    # endings
    if (i < len(en_lines)):
      ending_ja = re.search(b"(?:%[KkPpNn])+$", jap_line);
      ending_en = re.search(b"(?:%[KkPpNn])+$", en_lines[i]);
      if (ending_ja and ending_en and ending_ja.group() != ending_en.group()):
        en_lines[i] = en_lines[i][:ending_en.start()] + jap_line[ending_ja.start():];
        corrections += 1;
        # print ("ja: %s en: %s parts: %s ::: %s" % (ending_ja.group(), ending_en.group(), \
        #   en_lines[i][:ending_en.start()], jap_line[ending_ja.start():]));


  if corrections:
    print("Total automatic corrections:", corrections);

  if len(en_lines) != jap_entries_count:
    print("Entry count mismatch!", "Lines jap: %d(effective:%d), en: %d." % (len(jap_lines), jap_entries_count, len(en_lines)) );

  out_f = open(out, "wb");
  for i in range(len(jap_head)):
    out_f.write(jap_head[i]);


  for i in range(len(en_lines)):
    if i < jap_entries_count:
      out_f.write(jap_payload[i*3]);
      out_f.write(jap_payload[i*3+1]);
    if i < len(en_lines):
      out_f.write(en_lines[i]);
    #out_f.write("\n".encode("SHIFT-JIS"));
  out_f.close();
  jap_f.close();
  en_f.close();


if __name__ == '__main__':
  main();
