Scene files
============
TODO

Special Sequences
============

%N - New line

%K - wait for keypress

%P - pagebreak

%p - appears right before decision blocks.

%V - ???

%LC - Align to center

%LR - Align to right

%TS[3 digits][text]%TE - links text to TIPS

%FS[text]%FE - text fades in as 1 block, instead of letter-by-letter

%C[4 hex digits] - color

%T030 - delay? WARNING: On pc it has %T[\d\d] (2 digits) format, but on psp it needs to have 3 digits!

%X070 - Fixed offset from line start (also 010, 050 in game texts)

%XS[2 digits], %XE - %XS sets fixed character width. %XE resets it.

%n - ??? (in BOOT.BIN)

%S - ??? (in BOOT.BIN) (usually %n%S or %N%S)


BOOT.BIN
============

To disasm BOOT.BIN with prxtool:
`tools/prxtool -n tools/psp-NID-Prometheus.xml -o boot-disasm.txt -w workdir/BOOT.BIN`

`readelf -a BOOT.BIN` info about elf structure

Text occurrences:

Don't forget to add/subtract A0 to table values, which is an elf header size

table - text locations

12bb8c: - 12116c:1243d0(123fb0 jap) (approx) - section with text;
  0x12144c - scrolling menu text, delimited by new lines (%N), ends at 0x12871c.
136760:136aa0 - 12483с:128620
136ac0: sample text block, used in settings

137528:141520 - large empty area. Test if this can be used as an scratchpad/area for long strings.


The engine has a limit of 380 simultaneous characters on the scene, which causes crashes when the buffer is overflown. The workaround is to insert more %K%P sequences to the text.


init.bin
============

file has many(all?) same strings as the pc version of init.bin + all the TIPS + the chronology + other stuff

tables:
<br>
1140:1d38 - covers "names/init" section
<br>
7610:7f78 - TIPS
<br>
90dc:ac98 - Chronology

We skip all these sections:
```python3
    if 0x47f0 <= table_offs < 0x5350: continue
    if 0x7f90 <= table_offs < 0x871c: continue
    if 0x7520 <= table_offs < 0x7610: continue
```

ba68:dc40 names and init.txt content. This also is the first text occurrence in file.
<br>
dc40: - file names(don't modify!)
<br>
12b57:12ca3 - song-related stuff
<br>
12ca3:130ea - (Endings?)
<br>
130ea: - a strange untranstlated text block. Strings start with イラスト：左 (GoogTransl: 'Illustration:Left')
<br>
134de: - Song lyrics
<br>
14c30:2464c - Tips. They are ordered differently to the pc version.
<br>
26be8: - Chronology start
<br>

BTW, analyzing this file revealed that developers actually transliterated characters' names this way:
```
うしろのしょうめんのぼく／Uni
鏡の中のワタシ／Cocoro
天より墜ちたオレ／Satoru
```
(proof: 0x260a0 in init.bin)
So we might change these in the translation

Fonts
============

The game uses FONT00 (lzss-compressed .FOP), found in etc.afs, as a main font.

See folder `text/font/` for scripts.

Game engine adds to much width between glyphs (seems like 4px), so 
currently the right border was decreased by 2 px for all glyphs, which may 
cause some side effects.

Glyph 751 is a whitespace.

GIM format
============
Graphics format found in some T2P files after they are decompressed.
Can be converted to png with GimConv (Proprietary Sony tool, Google it).

TIM2 format
============

Graphics format found in some T2P files after they are decompressed.


Useful links:

HOME menu language: http://bbs.blacklabel-translations.com/showthread.php?tid=35&pid=84

TIM2 format: http://wiki.vg-resource.com/wiki/TIM2
