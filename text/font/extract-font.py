#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Extracts font metadata to a json

import sys
import os
from struct import *
from collections import namedtuple
import png


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
  'empty metadataOffset metadataSize \
  glyphsOffset glyphsSize blockSize \
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

  font = Font._make((fileHeader, [], allBytes[fileHeader.glyphsOffset:], allBytes))
  for i in range(glyphCount):
    glyphOffset = fileHeader.metadataOffset + (i * glyphMetadataStruct.size)
    glyphMetadata = glyphMetadataStruct.unpack_from(allBytes, glyphOffset)

    font.metadata.append(dict(l=glyphMetadata[0], r=glyphMetadata[1]))

  # print(font)
  return font

def writePng(font):
  # out = 'font00.png'
  raw = font.images

  bs = font.header.blockSize
  h = font.header.height
  w = font.header.width
  wb = bs // h
  BPP = 2

  glyphs = []
  for i in range(len(raw) // bs):
    pos = i * bs
    rawBlock = raw[pos:pos+bs]
    # 2 glyphs in every block
    glyph0 = []
    glyph1 = []
    for l in range(h):
      rawLine = rawBlock[ l*wb : l*wb+wb ]

      line0 = []
      line1 = []
      for p in range(wb // 2):
        # byte = rawLine[p]
        # px = ((byte & 1) << 1) | ((byte >> 1) & 1)
        # line0.append(px)
        # byte >>= 2
        # px = ((byte & 1) << 1) | ((byte >> 1) & 1)
        # line1.append(px)
        # byte >>= 2
        # px = ((byte & 1) << 1) | ((byte >> 1) & 1)
        # line0.append(px)
        # byte >>= 2
        # px = ((byte & 1) << 1) | ((byte >> 1) & 1)
        # line1.append(px)
        # Nope, let's try sth different

        loHalf = rawLine[p] & 0xF
        hiHalf = rawLine[p] >> 4 & 0xF
        px0 = loHalf & 0x3
        line0.extend([MagicPxConvert(loHalf & 0x3), MagicPxConvert(hiHalf & 0x3)])
        line1.extend([MagicPxConvert(loHalf >> 2), MagicPxConvert(hiHalf >> 2)])
      glyph0.append(line0)
      glyph1.append(line1)

    # block
    glyphs.append(glyph0)
    glyphs.append(glyph1)

  print("decoded glyphs count:", len(glyphs))
  print("Writing glyphs to files...")
  for i in range(0, len(glyphs)):
    writeGlyph(glyphs[i], i, w, h)


# Works both sides. I still have no idea why they did it though.
def MagicPxConvert(px):
  if (px & 0x1 == 1):
    px ^= 0x2
  return px


def writeGlyph(data, index, w, h):
  writer = png.Writer(w, h, greyscale=True, bitdepth=2)
  fname = 'glyphs/{0:d}.png'.format(index)
  file = open(fname, 'wb')
  writer.write(file, data)
  file.close()


def writeMetadata(font, path):
  f = open(path, "w")
  for i, v in enumerate(font.metadata):
    f.write("{0:5d}:: {1:5d} {2:d}\n".format(i, v['l'], v['r']))
  f.close()


def packFont(font, path):
  buf = bytearray(font.rawBytes)
  headerStruct.pack_into(buf, 0, *font.header)

  for i, v in enumerate(font.metadata):
    offset = font.header.metadataOffset + i * glyphMetadataStruct.size
    glyphMetadataStruct.pack_into(buf, offset, v['l'], v['r'])

  f = open(path, 'wb')
  f.write(buf)
  f.close()

def autotrim(font):
  # a dumb automatic width trim, 1px on each side
  for i, v in enumerate(font.metadata):
    if v['r'] > 0: v['r'] -= 1
    if v['l'] < font.header.width: v['l'] += 1

def main():
  path = "FONT00.FNT"
  if len(sys.argv) != 2:
    print('chose one of the args:')
    print('  png | extract - extracts all glyphs from FONT00.FNT file')
    print('  autotrim - trims all spaces between letters by 1px on both sides')
    exit(1)

  cmd = sys.argv[1] if len(sys.argv) > 1 else 'png'

  if (cmd == 'extract' or cmd == 'png'):
    os.makedirs('glyphs/', exist_ok=True)
    print('Extracting', path, 'to PNG')
    font = unpackFont(path);
    writeMetadata(font, 'glyphs/glyph_widths.txt')
    writePng(font)
  elif (cmd == 'autotrim'):
    print('Autotrimming everything by 1 px', path)
    font = unpackFont(path);
    autotrim(font)
    writeMetadata(font, 'autotrimmed_widths.txt')
    packFont(font, "FONT00.mod")
    print('Writing to FONT00.mod')
  

if __name__ == '__main__':
  main();
