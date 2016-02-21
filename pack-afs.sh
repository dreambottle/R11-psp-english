#!/bin/bash
ISO_RES_DIR=iso_extracted/PSP_GAME/USRDIR
ISO_BIN_DIR=iso_extracted/PSP_GAME/SYSDIR
WORKDIR=./workdir
COMPRESS=./compressbip

#mac.afs
for i in ./mac/*.SCN ; do
	echo $i
	f=`basename $i .SCN`
	$COMPRESS ./mac/$f.{SCN,BIP}
done
./repack_afs $WORKDIR/mac.afs $WORKDIR/mac-repacked.afs ./mac || exit 1;
mv -f $WORKDIR/mac-repacked.afs $ISO_RES_DIR/mac.afs



#etc.afs
#for i in ./etc/*.FNT ; do
#	echo $i
#	f=`basename $i .FNT`
#	$COMPRESS ./etc/$f.{FNT,FOP}
#done
#./repack_afs $WORKDIR/etc.afs $WORKDIR/etc-repacked.afs ./etc || exit 1;
#mv -f $WORKDIR/etc-repacked.afs $ISO_RES_DIR/etc.afs

#init.bin
INIT_SRC=init.dec.mod
if [ ! -f init.dec.mod ]; then
	# If modified file does not exist, just repack the original one.
	# Used for testing purposes
	INIT_SRC=init.dec
fi
$COMPRESS $WORKDIR/$INIT_SRC $WORKDIR/init.mod.bin || exit 1;
mv -f $WORKDIR/init.mod.bin $ISO_RES_DIR/init.bin


#BOOT.BIN
#TODO leave backup copy somewhere
echo Applying patches to BOOT.BIN
./tools/armips src/boot-patches.asm
#rm -f $ISO_BIN_DIR/BOOT.BIN
rm -f $ISO_BIN_DIR/EBOOT.BIN
cp -f $WORKDIR/BOOT.bin.patched $ISO_BIN_DIR/EBOOT.BIN
#cp -f $WORKDIR/BOOT.bin $ISO_BIN_DIR/BOOT.BIN #unnecessary
