# Project

**Remember 11 - the age of infinity** translation patches for PSP.

## Links

[**English Patch Downloads**](https://github.com/dreambottle/R11-psp-english/releases)

[Chinese release](https://bbs.oldmanemu.net/thread-5222.htm)

[Remember11 Explained](https://adayem.wordpress.com/) - analysis and explanations of game mysteries. Also provides a full walkthrough chart.

[Remember11 links on Fandom](http://remember11.fandom.com/wiki/Analysis_of_Remember_11) - other useful links

[Thread on Gbatemp.net](https://gbatemp.net/threads/release-remember11-the-age-of-infinity-psp-english-translation.470256/)

Credits for English translation: [TLWiki team](http://web.archive.org/web/20180819171103/https://tlwiki.org/?title=Remember11_-_the_age_of_infinity) (now defunct)


## Progress

**Finished**

Scenes: Fully translated, but text overflows the text box in some places. (Move the text box up a bit in game settings)
<br>
Shortcuts (init.bin): Fully translated
<br>
TIPS (init.bin): Fully translated. Starting from version 2, crashes are fixed.
<br>
Names (init.bin): Fully translated
<br>
Chronology (init.bin): Not translated in the English patch, Translated in the Chinese patch.
<br>
Menus (BOOT.BIN): Patched. HOME menu - Patched.
<br>
Font (FONT00.FOP) was tweaked for English text, reduced spacing. English glyphs were manually adjusted to be brighter and sharper for better legibility.


## For Developers

This project is a collection of scripts and programs written in bash, python and C.
- The Python and C programs unpack and repack game resources, decode text and fonts.
- Shell scripts are a very primitive build system that automates applying the translation. They will work on Linux (and probably macos).

For the full run:

1. Put the Remember11 iso at `iso/Remember11-jap.iso`

2. Run `./make.sh`

3. Result iso will be located at `iso/remember11-repacked.iso`

`./cleanup.sh` - to clean up intermediate files

`./generate-patches.sh` - to generate xdelta3 diff files.

Please refer to the content of shell scripts and source files for further details.
It was a learning project for me, so expect somewhat messy structure.


### Dependencies

The following tools should be available in PATH:

`7z mkisofs gcc python3`

Where to get:

- `mkisofs` is usually a part of `cdrtools` package.

- Brew command: `brew install p7zip cdrtools python3`.

- Arch Linux pacman install: `sudo pacman -S cdrtools 7zip python`.

Latest Python version tested: 3.14 (and will likely work with newer versions too.)
