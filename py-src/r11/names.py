#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import collections

TlNames = collections.namedtuple("TlNames", ["en", "cn"])
# key - original japanese name
# value - list of translated values [en, cn]
names_dict = {
  "？？": TlNames("??", "？？"),
  "こころ": TlNames("Kokoro", "心"),
  "悟": TlNames("Satoru", "悟"),
  "黛": TlNames("Mayuzumi", "黛"),
  "黄泉木": TlNames("Yomogi", "黄泉木"),
  "内海": TlNames("Utsumi", "内海"),
  "犬伏": TlNames("Inubushi", "犬伏"),
  "ゆに": TlNames("Yuni", "悠尼"),
  "穂鳥": TlNames("Hotori", "穗鸟"),
  "榎本": TlNames("Enomoto", "鼷本"),
  "男": TlNames("Man", "男"),
  "女": TlNames("Woman", "女"),
  "少年": TlNames("Boy", "男孩"),
  "少女": TlNames("Girl", "女孩"),
  "機長": TlNames("Pilot", "机长"),
  "みんな": TlNames("Everyone", "所有人"),
  # "Yukidoh", rather than "Yuukidou", because it is written everywhere else this way
  "ユウキドウ": TlNames("Yukidoh", "优希堂"),
  # These occur in init.bin only, but pasting them here, for reference
  "山岳救助隊員": TlNames("Mountain rescue worker", ";unused"),
  "沙也香": TlNames("Sayaka", ";unused"),
}

ja_original_separator = "・" # "\u30fb"
en_separator = ","
cn_separator = "、"

separators = TlNames(en_separator, cn_separator)

# tl_lang should be one of TlNames field names: "en" or "cn"
def translateNamesString(character_names: str, tl_lang: str) -> str:
  if not character_names:
    return ""
  
  jp_names = character_names.split(ja_original_separator)
  # print(jp_names, file=sys.stderr)
  translated_names = [names_dict.get(jp_name)._asdict()[tl_lang] for jp_name in jp_names]
  if (None in translated_names):
    raise Exception("Speaker translation for %s not found. Values: %s"%(character_names, translated_names))
  translated_names_joined = separators._asdict()[tl_lang].join(translated_names)
  return translated_names_joined
  
