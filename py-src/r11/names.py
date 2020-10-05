#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# key - original japanese name
# value - list of translated values [en, cn]
names = dict([
  ["？？", ["??", "？？"]],
  ["こころ", ["Kokoro", "心"]],
  ["悟", ["Satoru", "悟"]],
  ["黛", ["Mayuzumi", "黛"]],
  ["黄泉木", ["Yomogi", "黄泉木"]],
  ["内海", ["Utsumi", "内海"]],
  ["犬伏", ["Inubushi", "犬伏"]],
  ["ゆに", ["Yuni", "悠尼"]],
  ["穂鳥", ["Hotori", "穗鸟"]],
  ["榎本", ["Enomoto", "鼷本"]],
  ["男", ["Man", "男"]],
  ["女", ["Woman", "女"]],
  ["少年", ["Boy", "男孩"]],
  ["少女", ["Girl", "女孩"]],
  ["機長", ["Pilot", "机长"]],
  # "Yukidoh", rather than "Yuukidou", because it is written everywhere else this way
  ["ユウキドウ", ["Yukidoh", "优希堂"]],

  # These occur in init.bin only, but pasting them here, for reference
  ["山岳救助隊員", ["Mountain rescue worker", ";unused"]],
  ["沙也香", ["Sayaka", ";unused"]],
  ["みんな", ["Everyone", ";unused"]],
])

ja_original_separator = "・"
en_separator = ","
cn_separator = "、"
