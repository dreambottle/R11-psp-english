#!/bin/bash
ISO_RES_DIR=iso_extracted/PSP_GAME/USRDIR
ISO_BIN_DIR=iso_extracted/PSP_GAME/SYSDIR
WORKDIR=./workdir
COMPRESS=./compressbip

#mac.afs
for i in ./mac/*.SCN ; do
	f=`basename $i .SCN`
	$COMPRESS ./mac/$f.{SCN,BIP}
done
./repack_afs $WORKDIR/mac.afs $WORKDIR/mac-repacked.afs ./mac || exit 1;
mv -f $WORKDIR/mac-repacked.afs $ISO_RES_DIR/mac.afs

#etc.afs
./repack_afs $WORKDIR/etc.afs $WORKDIR/etc-repacked.afs ./etc || exit 1;
mv -f $WORKDIR/etc-repacked.afs $ISO_RES_DIR/etc.afs

#init.bin
#INIT_SRC=init.dec.mod
#if [ ! -f init.dec.mod ]; then
#	# If modified file does not exist, just repack the original one.
#	# Used for testing purposes
#	INIT_SRC=init.dec
#fi
#$COMPRESS $WORKDIR/$INIT_SRC $WORKDIR/init-edited.bin || exit 1;
#mv -f $WORKDIR/init-edited.bin $ISO_RES_DIR/init.bin

cp -f $WORKDIR/init.recompressed.bin $ISO_RES_DIR/init.bin

#BOOT.BIN
#TODO leave backup copy somewhere
tools/armipsd src/boot-patches.asm
#rm -f $ISO_BIN_DIR/BOOT.BIN
rm -f $ISO_BIN_DIR/EBOOT.BIN
cp -f $WORKDIR/BOOT.bin.patched $ISO_BIN_DIR/EBOOT.BIN
#cp -f $WORKDIR/BOOT.bin $ISO_BIN_DIR/BOOT.BIN #unnecessary
