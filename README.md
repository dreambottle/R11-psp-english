
This project ports the translation of **Remember 11 - the age of infinity** game to PSP.

If you know Japanese and want to improve some parts of this translation, talk to me [at gbatemp directly](https://gbatemp.net/members/dreambottle.384881/), or using the thread below.

[Thread on Gbatemp.net](https://gbatemp.net/threads/release-remember11-the-age-of-infinity-psp-english-translation.470256/)

[**Donwloads here**](https://github.com/dreambottle/R11-psp-english/releases)

Credits for English translation go to [TLWiki team](https://tlwiki.org/?title=Remember11_-_the_age_of_infinity)


Current status
-----------

Scenes: Ported - But text overflows the text box in some places. (Move the text box a bit up in game settings)
<br>
Shortcuts (init.bin): Ported.
<br>
TIPS (init.bin): Ported, but with bugs - there's too much English text in some of the tips. Those will either have unreadable parts, or crash the game.
<br>
Names (init.bin): Ported.
<br>
Chronology (init.bin): Not ported.
<br>
Menus (BOOT.BIN): Partial. Need translation help here, because text is different from the PC version. HOME menu - Done.
<br>
Font (FONT00.FOP): Tweaked for English text. Reduced width a bit. EN glyphs are brightened and sharpened.

Other Projects
-----------

I want to release a similar patch and sources of the tools for Ever 17 for English and, hopefully, Spanish and Russian translations. However, I can't give any timelines for this, because I do this in free time, whenever I have inspiration for it. Meanwhile, you can use [this patch, released by other fellas](https://gbatemp.net/threads/release-ever17-the-out-of-infinity-psp-english-translation.469362/).


For Developers
-----------

[Babun](http://babun.github.io/) (Windows/Cygwin) environment was used for developing and running this, but should work on linux/mac as well.

1. Put the Remember11 iso at `iso/Remember11-jap.iso`

2. Run `./make.sh`

3. Result iso will be at `iso/remember11-repacked.iso`

Tip: If you make any changes to the text or other resources, run ./repack-all.sh script to skip the "unpacking" phase.

##### Dependencies:

The following tools should be available on your PATH:

`7z mkisofs gcc python3`

`mkisofs` is a part of `cdrtools` package (google it).


##### Brew command for mac:

`brew install p7zip cdrtools python3`
