#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

import r11

# This is a very quick and dirty index builder for font character index, sjis code point and utf8 character

# should've used a class here, but the format of each entry in the returned list is [char, jis_code, unicode, comment]
def loadJapCjkCharsetAsIndex() -> list:
    font_table_len = 8192
    # index = [None] * font_table_len
    
    sjis_table_with_char_u8 = os.path.dirname(__file__) + "/../text/charset-tables/sjis-0213-2004-with-char-u8.txt"
    with open(sjis_table_with_char_u8, "r", encoding="utf-8-sig") as unicode_file:
        lines = unicode_file.readlines()
    
    lines = filter(lambda l: not l.startswith("##"), lines)

    ascii_lines_parsed = []
    cjk_lines_parsed = []
    for i, l in enumerate(lines):
        # ls = l.split("\t", 3)
        ls = l.split("\t", 4)
        char_utf8 = ls[0]
        char_jis_code = ls[1]
        char_unicode = ls[2]
        char_comment = ""
        # if len(ls) > 4 and "[200" in ls[4]:
        #    char_comment = ls[3] + " " + ls[4][:6]

        jis_bytes = bytearray.fromhex(char_jis_code[2:])

        # if ("[200" in l):
        #     char_utf8 = " "
        
        if (jis_bytes.__len__() == 2):
            # print(i, "char", char, "jis_bytes", jis_bytes)
            cjk_lines_parsed.append([char_utf8, char_jis_code, char_unicode, char_comment])
        else:
            ascii_lines_parsed.append([char_utf8, char_jis_code, char_unicode, char_comment])

    font_index = list(cjk_lines_parsed[:font_table_len])

    # print("len:", len(ascii_lines_parsed))

    # empty
    ranges_to_clear = [
        (108, 119),
        (127, 135),
        (142, 153),
        (168, 175),
        (183, 187),
        (188, 203),
        (213, 220),
        (246, 252),
        (278, 282),
        (494, 502),
        (526, 564),
        (597, 612),
        (645, 658),
        (690, 1128),
        (1220, 1410),
    ]
    for r in ranges_to_clear:
        for i in range(r[0], r[1]):
            font_index[i][0] = ""

    # em dash
    font_index[28][0] = "\u2015"
    font_index[28][2] = "U+2015"
    font_index[28][3] += "# Using U+2015 variant of em dash here - this is what python is converting to by default from SJIS"

    # Starting from glyph 751 are latin ASCII SJIS bytes [0x20 - 0x7D] (inclusive)
    for i in range(0x7E):
        # overwriting previous 0x20 bytes too because they aren't present in the font
        font_index[751-0x20 + i] = ascii_lines_parsed[i]
    font_index[751][3] = "# ASCII whitespace"
    # 845 - standard ascii "tilde" 0x7E ~
    font_index[845][0] = "~"
    font_index[845][1] = "0x7E"
    font_index[845][2] = ""
    font_index[845][3] = "# ASCII tilde"

    # 846-908 are SJIS 0xA1-0xDF
    for i in range(0xE0-0xA1):
        font_index[846 + i] = ascii_lines_parsed[0xA1 + i]

    # 1128 - circled number 1
    # ⑨
    font_index[1136][3] += "# R11:Rendered as a blank space (full width?)"
    # ä ö ü tm ...
    font_index[1137][0] = "ä"
    font_index[1138][0] = "ö"
    font_index[1139][0] = "ü"
    font_index[1145][0] = "™"
    #font_index[1146][0] = "…"
    # circled number 20
    font_index[1147][3] += "# R11: Rendered as a blank space (half width? or is it ideographic space U+3000?)"
    # see https://en.wikipedia.org/wiki/Whitespace_character for whitespace types breakdown

    # empty
    font_index[1182][0] = ""
    font_index[1209][0] = "∫"
    font_index[1211][0] = "∑"
    font_index[1212][0] = "√"
    # intersection, union
    font_index[1218][0] = "∩"
    font_index[1219][0] = "∪"

    # 1410: 0x889F 亜 - 1st block of cjk starts
    # 4374: 0x9872 腕 - last in the 1st block of cjk characters
    # 4375 - 4417 - should be empty
    for i in range(4375, 4418):
        font_index[i][0] = " "
    # 4418: 0x989F 弌 - 2nd block of cjk starts
    # 7807: 0xEAA4 熙 - last in the 2nd block of cjk
    for i in range(7808, font_table_len):
        font_index[i][0] = " "

    return font_index

def writeIndexAsText(index: list, path: str):
    with open(path, "w", encoding="utf8") as unicode_file:
        for i, l in enumerate(index):
            unicode_file.write("{}:\t{}\t{}\t{}\n".format(i, l[1], l[0], l[3]))

if __name__ == '__main__':
    index = loadJapCjkCharsetAsIndex()
    writeIndexAsText(index, os.path.dirname(__file__) + "/../text/charset-tables/r11-charset-index.txt")
