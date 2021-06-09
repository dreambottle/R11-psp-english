
This project ports the English translation of **Remember 11 - the age of infinity** VN to PSP.

Now also includes the Simplified Chinese translation.

### Useful Links

[**Patch Downloads**](https://github.com/dreambottle/R11-psp-english/releases)

[Chinese release](https://bbs.oldmanemu.net/thread-5222.htm)

[Thread on Gbatemp.net](https://gbatemp.net/threads/release-remember11-the-age-of-infinity-psp-english-translation.470256/)

[Remember11 Explained](https://adayem.wordpress.com/remember11-explained/) - explanation and analysis of the game mysteries, also has a full walkthrough chart.

[Remember11 links on Wikia](http://remember11.wikia.com/wiki/Analysis_of_Remember_11) - contains other useful links

Credits for English translation go to [TLWiki team](http://web.archive.org/web/20180819171103/https://tlwiki.org/?title=Remember11_-_the_age_of_infinity) (now defunct)


Current status
-----------

Scenes: Translated, but text overflows the text box in some places. (Move the text box up a bit in game settings)
<br>
Shortcuts (init.bin): Translated
<br>
TIPS (init.bin): Translated. Starting from version 2, crashes are fixed.
<br>
Names (init.bin): Translated
<br>
Chronology (init.bin): Not translated in English. Translated in Chinese.
<br>
Menus (BOOT.BIN): Translated. HOME menu - Translated.
<br>
Font (FONT00.FOP): Tweaked for English text, reduced spacing. EN glyphs are brightened and sharpened.


For Developers
-----------

This project is a bunch of scripts and programs in bash, python and C. Python and C programs unpack and repack game resources, decode text, fonts etc. Shell scripts automate the process of applying the translation. They should should work both on macos and linux.

For the full run

1. Put the Remember11 iso at `iso/Remember11-jap.iso`

2. Run `./make.sh`

3. Result iso will be at `iso/remember11-repacked.iso`

`./generate-patches.sh` can be used to generate xdelta3 diff files.

For further details, read the content of shell scripts (and other source files).

##### Dependencies:

The following tools should be available in your PATH:

`7z mkisofs gcc python3`

- `mkisofs` is a part of `cdrtools` package - google it.

- Brew command for macos to install dependencies: `brew install p7zip cdrtools python3`.

- Last tested to be working with python 3.8, likely works with later versions too.
