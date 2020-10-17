#!/usr/bin/env python3

import os
import re

import r11
import build_font_table as r11font


if __name__ == '__main__':
    # use original charset as a basis
    fontIndex = r11font.loadJapCjkCharsetAsIndex()

    cjk1Start = 1410
    cjk1End = 4375
    cjk2Start = 4418
    cjk2End = 7808

    cnCharactersFile = os.path.dirname(__file__) + "/../../text/tmp/cn-text-utf8/cjkchars.txt"
    cnCharactersStr = r11.readlines_utf8_crop_crlf(cnCharactersFile)[0]

    fontCodePoints = r11.str_to_r11_font_codepoints(cnCharactersStr, "en")

    # print(fontCodePoints)

    # some characters are the same - will attempt to preserve positions of those.
    fontCodePointsToPreserve = [cp for cp in fontCodePoints if cp >= 1410]
    fontCodePointsToPreserve = set(fontCodePointsToPreserve)
    # print(fontCodePointsToPreserve)

    newFontDict = dict()
    lastCodePoint = cjk1Start - 1
    for i, ch in enumerate(cnCharactersStr):
        assignedCodePoint = fontCodePoints[i]
        if assignedCodePoint != -1:
            newFontDict[assignedCodePoint] = ch
            continue

        # assign new codePoint
        lastCodePoint += 1
        while lastCodePoint in fontCodePointsToPreserve or cjk1End <= lastCodePoint < cjk2Start:
            lastCodePoint += 1
        fontCodePoints[i] = lastCodePoint
        newFontDict[lastCodePoint] = ch
    
    print(lastCodePoint)
    
    for i in range(cjk1Start, cjk2End):
        try :
            ch = newFontDict[i]
            fontIndex[i][0] = ch
        except KeyError:
            fontIndex[i][0] = ""
    
    r11font.writeIndexAsText(fontIndex, os.path.dirname(__file__) + "/../../text/charset-tables/r11-cn-font-table.txt")

