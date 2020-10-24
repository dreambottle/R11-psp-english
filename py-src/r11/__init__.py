import re
import sys
import os
from typing import List, NamedTuple, Tuple, Union

# CharsetElement = Tuple[int, bytes, str]
class CharsetElement(NamedTuple):
  charsetElement: int
  bytesequence: bytes
  character: str

# The original game font supports "JIS X 0208-1990" with some symbols from 2000.
# It is now best to use the charset conversion table (str_to_r11_bytes() function) generated for the game instead of standard python encodings
sjis_enc = "shift_jis_2004"
# sjis_enc = "sjis"

# chinese
# "GB2312"


r11_original_font_table_path: str = os.path.dirname(__file__) + "/../../text/charset-tables" + "/r11-orig-font-table.txt"
r11_cn_font_table_path: str = os.path.dirname(__file__) + "/../../text/charset-tables" + "/r11-cn-font-table.txt"

en_r11_charset_as_list: Union[List[CharsetElement], None] = None
en_r11_utf8_to_codes: dict = dict()
en_r11_bytes_to_codes: dict = dict()
cn_r11_charset_as_list: Union[List[CharsetElement], None] = None
cn_r11_utf8_to_codes: dict = dict()
cn_r11_bytes_to_codes: dict = dict()

# Detects trailing %K %P %p %N and %O (any combination)
trailing_control_vknop_re: re.Pattern = re.compile(r"\s*((?:%[VKNOPp]|%T\d{3})+)$")

def find_trailing_control_sequence(text: str) -> str:
  trailing_control_vknop = trailing_control_vknop_re.search(text)
  return trailing_control_vknop.group(0) if trailing_control_vknop else ""

# only removes %K %P %p %N and %O
def rm_trailing_control_sequence(line: str) -> str:
  line = trailing_control_vknop_re.sub("", line)
  return line

def clean_translation_enc_issues(line: str) -> str:
  line = re.sub("\uff5e", "\u301c", line) # two versions of fullwidth tilde '〜' (aka wave dash), but the 2nd one can be converted to sjis
  line = re.sub("\u2014", "\u2015", line) # likewise for em dash '—'
  line = re.sub("\u2013", "\u2015", line) # en dash '–' -> em dash '—'
  # fullwidth minus '－' -> em dash '—'
  # In JP and EN translation pulled from tlwiki it was used to blank out time, i.e. "午後－－時－－分：スフィアに戻る" "－:－－PM: returned to SPHIA",
  # but now the main text is cleaned up to use em dash in JP and regular dash in EN.
  # It is still incorrectly used in init.bin JP text and some CN tips
  line = re.sub("\uff0d", "\u2015", line)
  return line

def clean_cn_translation_line(line: str) -> str:
  line = clean_translation_enc_issues(line)
  line = re.sub("\u00B7", "\u30FB", line) # middle dot '·' -> katakana middle dot '・' (available in the font)
  return line

def clean_en_translation_line(line: str) -> str:
  line = clean_translation_enc_issues(line)
  line = re.sub(r"%(?![A-Za-z])", "\uff05", line) # replacing % metachar, with a lookalike char
  line = re.sub("\u2015\u2015", "\u2015", line) # double em dash '——' -> single em dash '—'
  # double spaces were fixed manually where appropriate, use text search to find remaining cases
  # line = re.sub(r"(?<!\b\S \S)  +", " ", line) # collapse multiple spaces unless there are also extra spaces within the neighboring words
  line = re.sub("\u00f6", "o", line) # ö no shift_jis for vowel+macron. which is strange considering that it's used by Hepburn
  # line = re.sub("\u014d", "o", line) # ō no shift_jis for vowel+macron. which is strange considering that it's used by Hepburn
  line = re.sub("\u00e9", "e", line) # é (utf8:c3a9) in fiancé; SA5_07, TIP_102
  line = re.sub("na\u00efve", "naive", line) # "naïve": no umlaut for i
  line = re.sub(r"''I''", "%CFF8FI%CFFFF", line) # colored text (yellow) to signify "ore", as deviated from Kokoro's normal "watashi".
  line = re.sub(r"'I'", "%C8CFFI%CFFFF", line) # colored text (blue) to signify "watashi", as deviated from Satoru's normal "ore".
  if "''" in line:
    exit("unmatched ''")
  # line = re.sub("\u2473", "\u2473", line) # ⑳ ('CIRCLED NUMBER TWENTY' (U+2473)). No need to replace, rendered as a wide space. (glyph #1147)
  # spaces are too thin on pc; Not the case for psp.

  return line


def println_sjis(line: str):
  sys.stdout.buffer.write(line.encode(sjis_enc))
  sys.stdout.buffer.write(b'\n')

def str_to_sjis_bytes(text: str, charset=sjis_enc) -> bytes:
  return text.encode(charset)

def sjis_bytes_to_str(sjisbytes: bytes, charset=sjis_enc) -> str:
  return sjisbytes.decode(charset)

def println_r11(text: str, lang = "en"):
  sys.stdout.buffer.write(str_to_r11_bytes(text, lang))
  sys.stdout.buffer.write(b'\n')

def str_to_r11_bytes(text: str, lang = "en", exception_on_unknown = False) -> bytes:
  (_, r11_utf8_to_codes, _) = _init_r11_charset(lang)
  r11_bytearray = bytearray()
  for ch in text:
    # regular whitespace
    if ch == ' ':
      r11_bytearray.extend(b'\x20')
    elif ch == '\n':
      r11_bytearray.extend(b'\n')
    else:
      try:
        r11_char_code = r11_utf8_to_codes[ch][1]
      except KeyError:
        if exception_on_unknown:
          raise Exception("character '{}' could not be mapped, lang {}".format(ch, lang))
        # print("r11 couldn't convert char:", ch, file=sys.stderr)
        r11_char_code = b'\x87\x40' #①
      r11_bytearray.extend(r11_char_code)
  return r11_bytearray

def r11_bytes_ro_str(r11bytes: bytes, lang = "en") -> str:
  (_, _, r11_bytes_to_codes) = _init_r11_charset(lang)
  r11_str = []
  for b in r11bytes:
    r11_str.extend(r11_bytes_to_codes[b][2])
  return "".join(r11_str)

def str_to_r11_font_codepoints(text: str, lang = "en") -> List[int]:
  (_, r11_utf8_to_codes, _) = _init_r11_charset(lang)
  fontIndices = []
  for ch in text:
    # regular whitespace - special handling (hardcoded)
    if ch == ' ':
      fontIndices.append(751)
      continue
    
    try:
      r11_char_code = r11_utf8_to_codes[ch][0]
      fontIndices.append(r11_char_code)
    except KeyError:
      # print("r11 couldn't convert char:", ch, file=sys.stderr)
      fontIndices.append(-1)
  return fontIndices

def _init_r11_charset(lang = "en"):  
  if lang == "en":
    global en_r11_charset_as_list
    global en_r11_utf8_to_codes
    global en_r11_bytes_to_codes
    if en_r11_charset_as_list != None:
      return (en_r11_charset_as_list, en_r11_utf8_to_codes, en_r11_bytes_to_codes)
    (en_r11_charset_as_list, en_r11_utf8_to_codes, en_r11_bytes_to_codes) = _load_r11_font_table(r11_original_font_table_path)
    return (en_r11_charset_as_list, en_r11_utf8_to_codes, en_r11_bytes_to_codes)
  elif lang == "cn":
    global cn_r11_charset_as_list
    global cn_r11_utf8_to_codes
    global cn_r11_bytes_to_codes
    if cn_r11_charset_as_list != None:
      return (cn_r11_charset_as_list, cn_r11_utf8_to_codes, cn_r11_bytes_to_codes)
    (cn_r11_charset_as_list, cn_r11_utf8_to_codes, cn_r11_bytes_to_codes) = _load_r11_font_table(r11_cn_font_table_path)
    return (cn_r11_charset_as_list, cn_r11_utf8_to_codes, cn_r11_bytes_to_codes)
  else:
    raise Exception("lang parameter not supported: '{}'".format(lang))

def _load_r11_font_table(r11_font_table_path) -> Tuple[List[CharsetElement], dict, dict]:
  r11_charset_lines = readlines_utf8_crop_crlf(r11_font_table_path)

  split = [x.split("\t", maxsplit=3) for x in r11_charset_lines]
  ## [<font code point>:int, <sjis sequence>:bytes, <utf8 char>:str]
  table_as_list = [CharsetElement(int(x[0][:-1]), bytes.fromhex(x[1][2:]), x[2]) for x in split]
  utf8_to_codes = dict()
  bytes_to_codes = dict()
  #validate and build dicts
  for i, v in enumerate(table_as_list):
    if i != v[0]:
      raise Exception("Charset index was not sequential")
    
    utf8_ch = v[2]
    r11_b = v[1]
    utf8_to_codes[utf8_ch] = v
    bytes_to_codes[r11_b] = v
  return (table_as_list, utf8_to_codes, bytes_to_codes)

def readlines_utf8_crop_crlf(filepath):
    with open(filepath, "r", encoding="utf-8-sig") as f:
        return [l.rstrip('\r\n') for l in f.readlines()]
