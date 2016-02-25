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

%T30 - delay? also produces white space

%X070 - (10, 50, 70 in game texts)???


BOOT.BIN
============

To disasm BOOT.BIN with prxtool:
`tools/prxtool -n tools/psp-NID-Prometheus.xml -o boot-disasm.txt -w workdir/BOOT.BIN`

Text occurrences:

0x121160 (approx) - section with text;
  0x12144c - scrolling menu text, delimited by new lines (%N), ends at 0x12871c.
0x136ac0: sample text block, used in settings


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
130ea: - some strange untranstlated text block. Strings start with イラスト：左 (GoogTransl: 'Illustration:Left')
<br>
134de: - Song lyrics
<br>
14c30:2464c - Tips. They do not seem to be ordered in the same way as the pc version(not sure).
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

The game uses FONT00, found (lzss-compressed .FOP) in etc.afs as a main font.
The format is not common and needs tools for conversion to be written.

The fonts are a little bit too large for the amount of text we have and need to have 1-2px less spacing between glyphs.
Or a smaller font in general, so that at least 4 lines can fit a regular textbox.


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