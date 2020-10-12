#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from os import path

import r11
import lib.chinese_converter as cconv
import build_font_table

# Temp script for testing how well existing font is suited for Chinese translation

text_file_path = "misc/cn/full-cn-script2.txt"
utf8_to_sjis_file_path = "misc/sjis-0213-2004-with-char-u8.txt"

def loadCnText() -> str:
    print("reading", text_file_path)
    with open(text_file_path, "r", encoding="utf8") as f_cn_script:
        cn_text = f_cn_script.read()
    
    print("Text characters: {}".format(cn_text.__len__()))

    cn_text = cn_text.replace("\n", "")
    cn_text = cn_text.replace(" ", "")
    cn_text = r11.clean_translation_enc_issues(cn_text)
    print("Text characters without linebreaks and spaces: {}".format(cn_text.__len__()))
    return cn_text


def loadCnText2() -> str:
    
    # load from initbin
    initbinTxtPath = path.dirname(__file__) + "/../text/other-psp-cn/init.bin.full.utf8.txt"
    with open(initbinTxtPath, "r", encoding="utf-8-sig") as f:
        initBinLines = f.readlines()[2:]
    initBinLines = [l.rstrip() for l in initBinLines if not l.startswith(";")]
    # initBinAll = "".join(initBinLines)

    # load from chapters
    #chaptersDir = path.dirname(__file__) + "/../text/chapters-psp/
    
    # load from boot
    # load from shortcut

# returns a list of [<char>, <count>] sorted by count desc
def buildUsageStatsListSorted(cn_text: str) -> list:
    cn_text_chars = list(cn_text)
    cn_text_chars.sort()

    character_stats = list()
    last = ''
    for v in cn_text_chars:
        if last == v:
            stat = character_stats.pop()
        else:
            stat = [v, 0]
        stat[1] += 1
        character_stats.append(stat)
        last = v
    character_stats.sort(key=lambda x: x[1])
    character_stats.reverse()
    return character_stats

def loadSjisCharactersList() -> list:
    # The provided file is a sjis-unicode mapping table.
    # The first character is a utf8-encoded character from sjis, order is same as in 
    print("reading", utf8_to_sjis_file_path)
    with open(utf8_to_sjis_file_path, "r", encoding="utf8") as unicode_sjis_file:
        lines = unicode_sjis_file.readlines()

    # table_lines = [l for l in lines if not l.startsWith("##")]
    table_lines = lines[186:] ## double-byte sjis characters start at this line
    characters_list = [l[0] for l in table_lines]
    return characters_list

def findConvertableAndNonConvertable(character_usage_stats: list) -> (list, list, int, int):
    converts = []
    non_converts = []
    converts_count = 0
    non_converts_count = 0
    for v in character_usage_stats:
        try:
            b = r11.str_to_sjis_bytes(v[0])
            s = r11.sjis_bytes_to_str(b)
            # print(s)
            converts.append(v)
            converts_count += v[1]
        except UnicodeEncodeError:
            non_converts.append(v)
            non_converts_count += v[1]
    return (converts, non_converts, converts_count, non_converts_count)

def findConvertableAndNonConvertableFromIndex(character_usage_stats: list, font_characters: set) -> (list, list, int, int):
    converts = []
    non_converts = []
    converts_count = 0
    non_converts_count = 0
    for v in character_usage_stats:
        if (font_characters.__contains__(v[0])):
            converts.append(v)
            converts_count += v[1]
        else:
            non_converts.append(v)
            non_converts_count += v[1]
    return (converts, non_converts, converts_count, non_converts_count)

def indexToSjisDict(font_index: []) -> dict:
    sjis_dict = dict()
    for i, entry in enumerate(font_index):
        utf8_char = entry[0]
        sjis_code = entry[1]
        if (sjis_code == " "):
            continue
        sjis_bytes = bytearray.fromhex(sjis_code[2:])
        # sjis_char = r11.sjis_bytes_to_str(sjis_bytes)
        # sjis_dict[sjis_char] = i
        # sjis_dict[utf8_char] = sjis_bytes
        sjis_dict[utf8_char] = i
    return sjis_dict

def saveCharacterIndices(characters, sjis_dict: dict, text_file_path):
    with open(text_file_path, "w", encoding="utf8") as file_to_write:
        for ch in characters:
            character = ch[0]
            index = sjis_dict.get(character, -1)
            file_to_write.write("{}: {}\n".format(index, character))



if __name__ == '__main__':
    cn_simp_text = loadCnText()

    font_index = build_font_table.loadJapCjkCharsetAsIndex()
    sjis_dict = indexToSjisDict(font_index)
    supported_jap_chars = set(sjis_dict.keys())

    cn_trad_text = cconv.to_traditional(cn_simp_text)

    cn_character_usage_stats_trad = buildUsageStatsListSorted(cn_trad_text)
    cn_character_usage_stats_simp = buildUsageStatsListSorted(cn_simp_text)
    cn_character_usage_stats = cn_character_usage_stats_trad

    print("Unique characters: {}".format(cn_character_usage_stats.__len__()))
    top_stats = cn_character_usage_stats[:10]
    top_characters = "".join(list(map(lambda x: x[0], top_stats)))
    print("Most used characters: {}\n{}".format(top_characters, top_stats))

    # (converts, non_converts, converts_count, non_converts_count) = findConvertableAndNonConvertable(cn_character_usage_stats)
    (converts, non_converts, converts_count, non_converts_count) = findConvertableAndNonConvertableFromIndex(cn_character_usage_stats, supported_jap_chars)

    print("    convertable characters: {} occurrences: {}".format(converts.__len__(), converts_count))
    print("non-convertable characters: {} occurrences: {}".format(non_converts.__len__(), non_converts_count))

    print("Most used non-convertable characters: \n{}".format(non_converts[:50]))

    # sjis_list = loadSjisCharactersList()
    # unused_sjis_set  = set(sjis_list)
    unused_sjis_set = set(supported_jap_chars)
    used_list_2 = []
    for c in converts:
        if not unused_sjis_set.__contains__(c[0]):
            if r11.str_to_sjis_bytes(c[0]).__len__() == 2:
                print("Not found in sjis list: {0}".format(c[0]))
                # else it's a single byte char and is ok because we skipped those already
        else:
            unused_sjis_set.remove(c[0])
            used_list_2.append(c[0])
    
    for c in non_converts:
        if unused_sjis_set.__contains__(c[0]):
            print("'unused' character was found in sjis list: {}".format(c[0]))
    
    print("unused sjis {}/{}".format(len(unused_sjis_set), supported_jap_chars.__len__()))
    
    used_list_2.sort()
    used_bytes = list([r11.str_to_sjis_bytes(x) for x in used_list_2])
    used_bytes.sort()
    print(used_bytes.__len__())

    (converts, non_converts, converts_count, non_converts_count) = findConvertableAndNonConvertableFromIndex(cn_character_usage_stats_simp, supported_jap_chars)
    saveCharacterIndices(converts, sjis_dict, "simp_convertable_character_indexes.txt")
    saveCharacterIndices(non_converts, sjis_dict, "simp_missing_characters.txt")
    (converts, non_converts, converts_count, non_converts_count) = findConvertableAndNonConvertableFromIndex(cn_character_usage_stats_trad, supported_jap_chars)
    saveCharacterIndices(converts, sjis_dict, "trad_convertable_character_indexes.txt")
    saveCharacterIndices(non_converts, sjis_dict, "trad_missing_characters.txt")

