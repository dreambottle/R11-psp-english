#!/bin/bash
ISO_RES_DIR=iso_extracted/PSP_GAME/USRDIR
ISO_BIN_DIR=iso_extracted/PSP_GAME/SYSDIR
WORKDIR=./workdir
COMPRESS=./compressbip
ARMIPS=./tools/armips
REPACK_SCENE=text/repack_scene.py

#mac.afs
mkdir -p mac-en/
for i in mac-en/*.SCN ; do
	echo Repacking $i
	f=`basename $i .SCN`
	$REPACK_SCENE text/mac-combined-psp/$f.txt mac/$f.SCN mac-en/$f.SCN
	$COMPRESS ./mac-en/$f.{SCN,BIP}
done
./repack_afs $WORKDIR/mac.afs $WORKDIR/mac-repacked.afs ./mac-en || exit 1;
mv -f $WORKDIR/mac-repacked.afs $ISO_RES_DIR/mac.afs



#etc.afs
#for i in etc-en/*.FNT ; do
#	echo $i
#	f=`basename $i .FNT`
#	$COMPRESS etc-en/$f.{FNT,FOP}
#done
if [ -f etc-en/FONT00.mod ]; then
$COMPRESS etc-en/FONT00.mod etc-en/FONT00.FOP
./repack_afs $WORKDIR/etc.afs $WORKDIR/etc-repacked.afs etc-en || exit 1;
mv -f $WORKDIR/etc-repacked.afs $ISO_RES_DIR/etc.afs
fi

#init.bin
INIT_SRC=init.dec.en
if [ ! -f init.dec.en ]; then
	# If modified file does not exist, just repack the original one.
	# Used for testing purposes
	INIT_SRC=init.dec
fi
$COMPRESS $WORKDIR/$INIT_SRC $WORKDIR/init.en.bin || exit 1;
mv -f $WORKDIR/init.en.bin $ISO_RES_DIR/init.bin


#BOOT.BIN
echo Applying patches to BOOT.BIN
cp -f $WORKDIR/BOOT.BIN.en $WORKDIR/BOOT.BIN.patched
$ARMIPS src/boot-patches.asm
#rm -f $ISO_BIN_DIR/BOOT.BIN
rm -f $ISO_BIN_DIR/EBOOT.BIN
cp -f $WORKDIR/BOOT.bin.patched $ISO_BIN_DIR/EBOOT.BIN
cp -f $WORKDIR/BOOT.bin.patched $ISO_BIN_DIR/BOOT.BIN
#cp -f $WORKDIR/BOOT.bin $ISO_BIN_DIR/BOOT.BIN #unnecessary
