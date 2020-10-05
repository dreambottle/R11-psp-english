import re
import sys
import os

# The original game font supports "JIS X 0208-1990" with some symbols from 2000.
# It is now best to use the charset conversion table that I generated for the game instead of standard python encodings
sjis_enc = "shift_jis_2004"
# sjis_enc = "sjis"

# chinese
# "GB2312"


r11_original_charset_table_path: str = os.path.dirname(__file__) + "/../../text/charset-tables" + "/r11-glyph-sjis-utf8-index.txt"
r11_charset_as_list: [int, bytes, str] = None
r11_utf8_to_codes: dict = dict()
r11_bytes_to_codes: dict = dict()

# Detects trailing %K %P %p %N and %O (any combination)
trailing_meta_re_str = r"\s*((?:%[VKNOPp]|%T\d{3})+)$"
trailing_meta_re: re.Pattern = re.compile(trailing_meta_re_str)

def findTrailingControlSequence(text: str) -> str:
  trailing_meta = trailing_meta_re.search(text)
  return trailing_meta.group(0) if trailing_meta else ""

# only removes %K %P %p %N and %O
def rmTrailingControlSequence(line: str) -> str:
  line = trailing_meta_re.sub("", line)
  return line

def clean_translation_enc_issues(line: str) -> str:
  line = re.sub("\uff5e", "\u301c", line) # two versions of fullwidth tilde '〜' (aka wave dash), only one of which has a shift_jis codepoint
  line = re.sub("\u2014", "\u2015", line) # likewise for em dash '—'
  line = re.sub("\u2013", "\u2015", line) # en dash '–' -> em dash '—'
  return line

def clean_en_translation_line(line: str) -> str:
  line = clean_translation_enc_issues(line)
  line = re.sub(r"%(?![A-Z])", "\uff05", line) # replacing % metachar, with a lookalike char
  line = re.sub("\u2015\u2015", "\u2015", line) # double em dash '——' -> single em dash '—'
  line = re.sub("\uff0d", "-", line) # fullwidth minus '―' -> hyphen '-'. In JP and EN translation was used to blank out time, i.e. "午後－－時－－分：スフィアに戻る" "－:－－PM: returned to SPHIA"
  # double spaces were fixed manually where appropriate, use text search to find remaining cases
  # line = re.sub(r"(?<!\b\S \S)  +", " ", line) # collapse multiple spaces unless there are also extra spaces within the neighboring words
  line = re.sub("\u00f6", "o", line) # ö no shift_jis for vowel+macron. which is strange considering that it's used by Hepburn
  line = re.sub("\u014d", "o", line) # no shift_jis for vowel+macron. which is strange considering that it's used by Hepburn
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

def println_r11(text: str):
  sys.stdout.buffer.write(str_to_r11_bytes(text))
  sys.stdout.buffer.write(b'\n')

def str_to_r11_bytes(text: str) -> bytes:
  global r11_utf8_to_codes
  init_r11_charset()
  r11_bytearray = bytearray()
  for ch in text:
    # regular whitespace
    if ch == ' ':
      r11_bytearray.extend(b'\x20')
    else:
      r11_utf8_to_codes.__contains__(ch)
      try:
        r11_char_code = r11_utf8_to_codes[ch][1]
      except KeyError:
        # print("r11 couldn't convert char:", ch, file=sys.stderr)
        r11_char_code = b'\x87\x40' #①
      r11_bytearray.extend(r11_char_code)
  return r11_bytearray

def r11_bytes_ro_str(r11bytes: bytes) -> str:
  global r11_bytes_to_codes
  init_r11_charset()
  r11_str = []
  for b in r11bytes:
    r11_str.extend(r11_bytes_to_codes[b][2])
  return "".join(r11_str)

def init_r11_charset():
  global r11_charset_as_list
  global r11_utf8_to_codes
  global r11_bytes_to_codes
  if r11_charset_as_list != None:
    return
  
  with open(r11_original_charset_table_path, "r", encoding="utf-8-sig") as r11_charset_file:
    r11_charset_lines = r11_charset_file.readlines()

  split = [x.split(" ", maxsplit=2) for x in r11_charset_lines]
  ## [<font code point>:int, <sjis sequence>:bytes, <utf8 char>:str]
  # for i, x in enumerate(split):
  #   print("split[",i,"]=", split[i], file=sys.stderr)
  #   print("parsed 0 [",i,"]=", int(split[i][0][:-1]), file=sys.stderr)
  #   print("parsed 1 [",i,"]=", bytes.fromhex(split[i][1][2:]), file=sys.stderr)
  #   print("parsed 2 [",i,"]=", split[i][2][:1], file=sys.stderr)
  parsed = [[int(x[0][:-1]), bytes.fromhex(x[1][2:]), x[2][:1]] for x in split]
  r11_charset_as_list = list(parsed)

  #validate and build dict
  for i, v in enumerate(r11_charset_as_list):
    if i != v[0]:
      raise Exception("Charset index was not sequential")
    
    utf8_ch = v[2]
    r11_b = v[1]
    r11_utf8_to_codes[utf8_ch] = v
    r11_bytes_to_codes[r11_b] = v
  return r11_charset_as_list
