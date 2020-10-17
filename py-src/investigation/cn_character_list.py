#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# generates a list of characters for the cn font

import os
import re

import r11


def readlines_utf8_crop_crlf(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return [l.rstrip('\r\n') for l in f.readlines()]

if __name__ == '__main__':
    initbin = os.path.dirname(__file__) + "/../../text/tmp/cn-text-utf8/initbin.txt"
    boot = os.path.dirname(__file__) + "/../../text/tmp/cn-text-utf8/boot.txt"
    script = os.path.dirname(__file__) + "/../../text/tmp/cn-text-utf8/fullscript.txt"
    shortcut = os.path.dirname(__file__) + "/../../text/tmp/cn-text-utf8/shortcut.txt"

    listSaveAs = os.path.dirname(__file__) + "/../../text/tmp/cn-text-utf8/cjkchars.txt"
    
    initbinTxt = readlines_utf8_crop_crlf(initbin)[0]
    bootTxt = readlines_utf8_crop_crlf(boot)[0]
    scriptTxt = readlines_utf8_crop_crlf(script)[0]
    shortcutTxt = readlines_utf8_crop_crlf(shortcut)[0]

    allTxt = initbinTxt + bootTxt + scriptTxt + shortcutTxt
    allTxt = r11.clean_cn_translation_line(allTxt)

    charSet = set()
    for character in allTxt:
        charSet.add(character)

    charsetFilteredList = [c for c in charSet if not (0 <= r11.str_to_r11_font_indices(c, lang="cn")[0] < 1410)]
    charsetFilteredList.sort()

    print("charset len", len(charsetFilteredList))
    print("charset:", charsetFilteredList)

    # charsetNewList = [c for c in charsetFilteredList if r11.str_to_r11_font_indices(c, lang="cn")[0] == -1]
    # print("charset new len", len(charsetNewList))
    # print("charset new:", charsetNewList)

    with open(listSaveAs, "w", encoding="utf-8-sig") as f:
        f.write("".join(charsetFilteredList))
