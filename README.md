
This project ports the translation of **Remember 11 - the age of infinity** game to PSP.

If you know Japanese and want to improve some parts of this translation, contact me [at gbatemp directly](https://gbatemp.net/members/dreambottle.384881/), or in the thread, listed below.

### Useful Links

[**Patch Downloads**](https://github.com/dreambottle/R11-psp-english/releases)

[Thread on Gbatemp.net](https://gbatemp.net/threads/release-remember11-the-age-of-infinity-psp-english-translation.470256/)

[Remember11 Explained](https://adayem.wordpress.com/remember11-explained/) - explanation and analysis of the game mysteries, also has a full walkthrough chart.

[Remember11 links on Wikia](http://remember11.wikia.com/wiki/Analysis_of_Remember_11) - contains other useful links

Credits for English translation go to [TLWiki team](https://tlwiki.org/?title=Remember11_-_the_age_of_infinity)


Current status
-----------

Scenes: Ported - But text overflows the text box in some places. (Move the text box a bit up in game settings)
<br>
Shortcuts (init.bin): Ported.
<br>
TIPS (init.bin): Ported. Starting from version 2, crashes are fixed.
<br>
Names (init.bin): Ported.
<br>
Chronology (init.bin): Not ported.
<br>
Menus (BOOT.BIN): Partial. Need help with translation here, because text is different from the PC version. HOME menu - Done.
<br>
Font (FONT00.FOP): Tweaked for English text. Reduced width a bit. EN glyphs are brightened and sharpened.

Other Projects
-----------

I want to release a similar patch and sources of the tools for Ever 17 for English and, hopefully, Spanish and Russian translations. However, I can't give any timelines for this, because I do this in free time, whenever I have inspiration for it. Meanwhile, you can use [this patch, released by other fellas](https://gbatemp.net/threads/release-ever17-the-out-of-infinity-psp-english-translation.469362/).


For Developers
-----------

This project contains a bunch of scripts and programs written in shell script, python3 and C, which automate the process of applying translation. I ran this on macos, but should work on linux as well.

1. Put the Remember11 iso at `iso/Remember11-jap.iso`

2. Run `./make.sh`

3. Result iso will be at `iso/remember11-repacked.iso`

Afterwards, `./generate-patches.sh` can be run in order to generate xdelta3 diff files.

For further details, read the contents of shell scripts (and other source files).

Tip: After you've made changes to the text or other resources, run `./repack-all.sh` script to skip the "unpacking" phase and repack changes.

##### Dependencies:

The following tools should be available on your PATH:

`7z mkisofs gcc python3`

- `mkisofs` is a part of `cdrtools` package - google it.

- Brew command for macos: `brew install p7zip cdrtools python3`

- Last tested to be working with python v3.7.0
