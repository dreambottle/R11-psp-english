#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from struct import *
from collections import namedtuple
import png

GLYPH_DATA_FILE = 'glyph_data.txt'

Font = namedtuple('Font', ['header','metadata','imageRawData','rawBytes'])

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
Header = namedtuple('Header', [
  'empty',
  'metadataOffset', 'metadataSize',
  'glyphsOffset', 'glyphsSize',
  'blockSize', 'magic1', 'width', 'height', 'magic2'])
headerStruct = Struct('<8sIIIIHBBBB')

# Left and right borders of the glyph, in px. The count goes from the left for both values. 
# Glyphs count in FONT00 - 8192
# GlyphMetadata = namedtuple('GlyphMetadata', ['l', 'r'])
glyphMetadataStruct = Struct('<BB')


def unpackFont(path):
  glyphsPerBlock = 2

  f=open(path, "rb")
  allBytes = f.read()
  f.close()

  fileHeader = Header._make(headerStruct.unpack_from(allBytes, 0))
  print("Header:", fileHeader)
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

def packFont(font, path, pngGlyphPath = None):
  buf = bytearray(font.header.glyphsOffset)
  headerStruct.pack_into(buf, 0, *font.header)

  for i, v in enumerate(font.metadata):
    offset = font.header.metadataOffset + i * glyphMetadataStruct.size
    glyphMetadataStruct.pack_into(buf, offset, v['l'], v['r'])

  f = open(path, 'wb')
  f.write(buf)
  f.write(font.imageRawData)
  f.close()

def writePngs(font, firstHalfHack=False):
  # out = 'font00.png'
  raw = font.imageRawData

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
      rng = wb
      if firstHalfHack:
        rng //= 2
      for p in range(rng):
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
        line0.extend([magicPxConvert(loHalf & 0x3), magicPxConvert(hiHalf & 0x3)])
        line1.extend([magicPxConvert(loHalf >> 2), magicPxConvert(hiHalf >> 2)])
      glyph0.append(line0)
      glyph1.append(line1)
    # every block
    glyphs.append(glyph0)
    glyphs.append(glyph1)

  print("decoded glyphs count:", len(glyphs))
  print("Writing glyphs to files...")
  writer = png.Writer(w, h, greyscale=True, bitdepth=2)
  for i in range(0, len(glyphs)):
    file = open('glyphs/{0:d}.png'.format(i), 'wb')
    writer.write(file, glyphs[i])
    file.close()


# Works both ways (encode & decode). I still have no idea why they did it though.
def magicPxConvert(px):
  if (px & 0x1 == 1):
    px ^= 0x2
  return px


def writeMetadata(font, path):
  f = open(path, "w")
  f.write("count: {0:d}\n".format( len(font.metadata) ))
  f.write("width: {0:d}\n".format(font.header.width))
  f.write("height: {0:d}\n".format(font.header.height))
  f.write("blockSize: {0:d}\n".format(font.header.blockSize))
  for i, v in enumerate(font.metadata):
    f.write("{0:5d}: {1:d}:{2:d}\n".format(i, v['l'], v['r']))
  f.close()

def parseMetadata(path):
  with open(path, 'r') as f:
    count = int( f.readline().split(':')[1].strip() )
    width = int( f.readline().split(':')[1].strip() )
    height = int( f.readline().split(':')[1].strip() )
    bs = int( f.readline().split(':')[1].strip() )

    metadataOffset = 0x1E
    metadataSize = count*2 # 2 bytes per glyph
    glyphsOffset = metadataOffset + metadataSize
    if (glyphsOffset & 0xFFF != 0):
      glyphsOffset = (glyphsOffset + 0x1000) & ~0xFFF
    glyphsSize = count//2 * bs # 2 glyphs per block
    # 'empty',
    # 'metadataOffset', 'metadataSize',
    # 'glyphsOffset', 'glyphsSize',
    # 'blockSize', 'magic1', 'width', 'height', 'magic2'
    header = Header(bytes(8), metadataOffset, metadataSize,
      glyphsOffset, glyphsSize,
      bs, 0x5, width, height, 0)

    metadata = []
    for i in range(count):
      values = [int(s.strip()) for s in f.readline().split(':')]
      if (values[0] != i):
        print('Metadata mismatch at index {0}: got {1}'.format(i, values[0]))
        break
      metadata.append(dict(l=values[1], r=values[2]))
    return (header, metadata)


def generateFont(dir):
  header, metadata = parseMetadata("{0}/{1}".format(dir, GLYPH_DATA_FILE))
  count = len(metadata)
  imageData = bytearray((count//2) * header.blockSize)
  pngfmt = '{0}/{1}.png'
  for i in range(0, count, 2):
    block = pngsToRawGlyphBlock(header.blockSize,
              pngfmt.format(dir, i), pngfmt.format(dir, i+1))
    imageData[(i//2)*header.blockSize : (i//2)*header.blockSize+header.blockSize] = block

  return Font(header, metadata, imageData, [])

def pngsToRawGlyphBlock(blockSize, pngPath0, pngPath1):
  rawData = bytearray(blockSize)
  r0 = png.Reader(filename=pngPath0)
  r1 = png.Reader(filename=pngPath1)
  pngMaps = (r0.read(), r1.read())

  if (pngMaps[0][0] != pngMaps[1][0]) or (pngMaps[0][1] != pngMaps[1][1]):
    print("Dimensions mismatch between {0} and {1}".format(pngPath0, pngPath1))
    exit(1)
  if pngMaps[0][3]['bitdepth'] != 2 or pngMaps[1][3]['bitdepth'] != 2:
    print("Bitdepth must be 2! (files: {0} {1})".format(pngPath0, pngPath1))
    exit(1)
  
  BPP = 2
  w = pngMaps[0][0]
  h = pngMaps[0][1]
  bytesPerLineImg = (2 * w * BPP) // 8
  bytesPerLineBlock = blockSize // h
  pixels = (list(pngMaps[0][2]), list(pngMaps[1][2]))
  for l in range(h):
    for nbyte in range(bytesPerLineImg):
      npx = nbyte * 2
      # lo to hi
      px = [
        pixels[0][l][npx],
        pixels[1][l][npx],
        pixels[0][l][npx+1],
        pixels[1][l][npx+1]
      ]
      byte = 0
      # doing the magic conversion and packing into a byte
      for i, p in enumerate(px): byte |= magicPxConvert(p) << 2*i
      rawData[l*bytesPerLineBlock+nbyte] = byte
  return rawData


def autotrim(font):
  # a dumb automatic width trim.
  for i, v in enumerate(font.metadata):
    # if v['l'] < font.header.width: v['l'] += 1
    if v['r'] > 0: v['r'] -= 2


def main():
  REPACKEDPATH = "FONT00.NEW"

  if len(sys.argv) < 2:
    print('chose one of the args:')
    print('  png|pnghalf [<FONT00.FNT>] - extracts all glyphs from FONT00.FNT file (pnghalf only extracts left half of the image)')
    print('  autotrim [<FONT00.FNT>] - trims all spaces between letters by 1px on both sides')
    print('  repack <dir> - packs pngs and metadata in <dir> into a "%s" font file'%(REPACKEDPATH))
    exit(1)

  cmd = sys.argv[1]
  srcpath = sys.argv[2] if len(sys.argv) > 2 else 'FONT00.FNT'
  
  if (cmd == 'png' or cmd == 'pnghalf'):
    os.makedirs('glyphs/', 0o755, exist_ok=True)
    print('Extracting', srcpath, 'to PNG')
    font = unpackFont(srcpath);
    writeMetadata(font, 'glyphs/{0}'.format(GLYPH_DATA_FILE))
    writePngs(font, firstHalfHack=(cmd == 'pnghalf'))
  elif (cmd == 'autotrim'):
    print('Autotrimming everything by 2 px', srcpath)
    font = unpackFont(srcpath);
    autotrim(font)
    writeMetadata(font, GLYPH_DATA_FILE)
    print('Writing to', 'FONT00.MOD')
    packFont(font, 'FONT00.MOD')
  elif (cmd == 'repack'):
    if len(sys.argv) <= 2: exit('Not enough args')
    print('Generating the font')
    font = generateFont(srcpath)
    print('Writing to', REPACKEDPATH)
    packFont(font, REPACKEDPATH)
  

if __name__ == '__main__':
  main();
