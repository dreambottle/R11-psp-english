
The goal of this project is to port the translation of the Remember 11 game to psp.

Help wanted in hacking and testing!

*Contributions are welcome!*

Current status:

Scenes: Yes - But text overflows the windows in some places. (Crashes are expected)
<br>
Shortcuts (init.bin): Yes.
<br>
TIPS (init.bin): Transferred, but it will very likely overflow the screen.
<br>
Names (init.bin): Yes.
<br>
Chronology (init.bin): No.
<br>
Menus (BOOT.BIN): Partial. Need translation help, because these strings are different from the PC version. HOME menu - Yes.
<br>
Font (FONT00.FOP): Autotrimmed by 2px. Wrote repackaging scripts to potentially replace the font.

How To Use This
-----------

[Babun](http://babun.github.io/) (Windows/Cygwin) environment was used for developing and running this, but should work on linux/mac as well.

1. Put the Remember11 iso at `iso/Remember11-jap.iso`

2. Run `./make.sh`

3. Result iso will be at `iso/remember11-repacked.iso`


If you make any changes to the text or other resources, run ./repack-all.sh script to skip the "unpacking" phase.

Dependencies
----------

The following tools should be available on your PATH:

`7z mkisofs gcc perl python3`

`mkisofs` is a part of `cdrtools` package.

Also you will need to install File::Slurp module for Perl:<br>
`cpan File::Slurp`


##### Brew install command for mac:

`brew install p7zip cdrtools python3` 