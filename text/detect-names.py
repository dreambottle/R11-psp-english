#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

def main():
  fdir = "chapters-psp/"
  files = os.listdir(fdir)

  names = set()
  opening_quote = "「"

  for fname in files:
    f = open(fdir+fname, "r", encoding="utf8")
    lns = f.readlines()
    f.close()
    f_names = [ln.split(opening_quote, 1)[0] for ln in lns \
                if (opening_quote in ln) and not ln.startswith("%")]
    names.update(f_names)

  for n in names:
    print(n)


if __name__ == '__main__':
  main();
