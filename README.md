
The goal of this project is to port the translation of the Remember 11 game to psp.

Help wanted in hacking and testing!

*Contributions are welcome!*

Current status:

Scenes: Yes - But text often overflows the windows. Crashes are expected until text is fixed.
<br>
(init.bin) TIPS: No
<br>
(init.bin) Names: Yes (together with other content from the PC version of init.bin), however the name box still doesn't seem to work.
<br>
(init.bin) Chronology: No
<br>
(BOOT.BIN) Menus: Partial. Need translation help, because these strings are different from the PC version. HOME menu - Yes.


How To
-----------

[Babun](http://babun.github.io/) (Windows/Cygwin) environment was used for developing and running this, but should work on linux/mac as well.

1. The Remember11 iso should be at `iso/Remember11-jap.iso`

2. Run `./make.sh`

3. Result iso will be at `iso/remember11-repacked.iso`.


If you make any changes to the text or other resources, run ./repack-all.sh script to skip the "unpacking" phase.

Dependencies:
----------

The following tools should be available:

`p7zip mkisofs gcc perl python3`

You will need to install File::Slurp module for Perl:<br>
`cpan File::Slurp`

If you're on mac/linux you will need to compile [armips](https://github.com/Kingcom/armips) for patching BOOT.BIN and put it into `tools/`. (I only did this for Windows)
