#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Extracts font metadata to a json 

import sys
from struct import *
from collections import namedtuple

Font = namedtuple('Font', 'header metadata images rawBytes')

# Little-endian byte order
# 00: 8 bytes - zeroes
# 08: int32 - font widths offset
# 0c: int32 - font widths size
# 10: int32 - glyph data offset
# 14: int32 - glyph data size
# 18: int16 - 100h - glyph pair size
# 1a: 4 bytes:
#   5h - ?, 10h - glyph height, 10h - glyph width, 0 - ?
# 
# https://docs.python.org/3/library/struct.html#format-characters
Header = namedtuple('Header',
  'empty metadataOffset metadataSize glyphsOffset \
  glyphsSize blockSize \
  magic1 height width magic2')
headerStruct = Struct('<8sIIIIHBBBB')

# Glyphs count in FONT00 - 8192
GlyphMetadata = namedtuple('GlyphMetadata', 'l r')
glyphMetadataStruct = Struct('<BB')

# no image extraction yet
def unpackFont(path):
  glyphsPerBlock = 2

  f=open(path, "rb")
  allBytes = f.read()
  f.close()

  fileHeader = Header._make(headerStruct.unpack_from(allBytes, 0))
  print("Header:", headerStruct.unpack_from(allBytes, 0), fileHeader)
  blockCount = fileHeader.glyphsSize // fileHeader.blockSize
  print("Block count:", blockCount)
  
  glyphCount = blockCount * glyphsPerBlock
  print("Glyph count:", glyphCount)

  font = Font._make((fileHeader, [], [], allBytes))
  for i in range(glyphCount):
    glyphOffset = fileHeader.metadataOffset + (i * glyphMetadataStruct.size)
    glyphMetadata = glyphMetadataStruct.unpack_from(allBytes, glyphOffset)

    font.metadata.append(dict(l=glyphMetadata[0], r=glyphMetadata[1]))

  # print(font)
  return font

def packFont(font, path):
  buf = bytearray(font.rawBytes)
  # buf = BufferedWriter()
  # font.rawBytes[:font.header.size] = (font.header)
  headerStruct.pack_into(buf, 0, *font.header)

  for i, v in enumerate(font.metadata):
    if (i > 100 and i < 300):
      print(i, v)
    offset = font.header.metadataOffset + i * glyphMetadataStruct.size
    glyphMetadataStruct.pack_into(buf, offset, v['l'], v['r'])

  f = open(path, 'wb')
  f.write(buf)
  f.close()

def main():
  path = sys.argv[1] if len(sys.argv) > 1 else "FONT00.FNT"
  font = unpackFont(path);

  # a dumb automatic width trim, 1px on each side
  for i, v in enumerate(font.metadata): 
    if v['r'] > 0: v['r'] -= 1
    if v['l'] < font.header.width: v['l'] += 1

  packFont(font, "FONT00.mod")

if __name__ == '__main__':
  main();
