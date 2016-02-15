#!/bin/bash
# extract all the japanese gametext.
# this script only has to be run once, it isn't part of the patcher.
GIMCONV="./tools/GimConv/GimConv.exe"
UNBIP="./decompressbip"
AFSDIR="iso_extracted/PSP_GAME/USRDIR"

unpack_afs () {
	./repack_afs $AFSDIR/$PKG.afs /dev/null /dev/null $PKG/ || exit 1
}

PKG=mac
unpack_afs
for i in $PKG/*.BIP ; do
	f=`basename $i .BIP`
	$UNBIP $PKG/$f{.BIP,.SCN} || exit 1
done

PKG=etc
unpack_afs
for i in $PKG/*.T2P ; do
	f=`basename $i .T2P`
	$UNBIP $PKG/$f{.T2P,.GIM} || exit 1
	$GIMCONV $PKG/$f.GIM -o $f.png -r11
done
for i in $PKG/*.FOP ; do
	f=`basename $i .FOP`
	$UNBIP $PKG/$f{.FOP,.FNT} || exit 1
	#$GIMCONV $PKG/$f.FNT -o $f.png -r11
done
# todo omit maskXXX.T2P files - those are of TIM2 format and not required
rm -f $PKG/mask*.GIM

