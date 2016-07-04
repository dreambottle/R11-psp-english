#!/bin/bash
# extract all the japanese gametext.
# 
GIMCONV="./tools/GimConv/GimConv.exe"
DECOMPRESS="./bin/decompressbip"
REPACK_AFS="./bin/repack_afs"

RES_DIR="iso_extracted/PSP_GAME/USRDIR"
WORK_DIR="./workdir"


unpack_afs () {
	echo Unpacking $1.afs
	$REPACK_AFS $WORK_DIR/$1.afs /dev/null /dev/null $1/ || exit 1
}

mkdir -p $WORK_DIR
mv iso_extracted/PSP_GAME/SYSDIR/BOOT.BIN $WORK_DIR/BOOT.BIN
#mv iso_extracted/PSP_GAME/SYSDIR/EBOOT.BIN $WORK_DIR/EBOOT.BIN

cp $RES_DIR/mac.afs $WORK_DIR/mac.afs
cp $RES_DIR/etc.afs $WORK_DIR/etc.afs
cp $RES_DIR/init.bin $WORK_DIR/init.bin

PKG=mac
rm -rf $PKG/
unpack_afs $PKG
for i in text/chapters-psp/[A-Z0-9]*_[0-9]*.txt ; do
	f=`basename $i .txt`
	$DECOMPRESS $PKG/$f{.BIP,.SCN} || exit 1
done
$DECOMPRESS $PKG/SHORTCUT{.BIP,.SCN} || exit 1

PKG=etc
rm -rf $PKG/
unpack_afs $PKG
#for i in $PKG/*.T2P ; do
#	f=`basename $i .T2P`
#	$DECOMPRESS $PKG/$f{.T2P,.GIM} || exit 1
#	$GIMCONV $PKG/$f.GIM -o $f.png -r11
#done
for i in $PKG/*.FOP ; do
	f=`basename $i .FOP`
	$DECOMPRESS $PKG/$f{.FOP,.FNT} || exit 1
	#mv -f $PKG/$f.FNT $WORK_DIR/$f.FNT
	#TODO convert font to editable format
done
cp etc/FONT00.FNT text/font/FONT00.FNT 

$DECOMPRESS $WORK_DIR/init.bin $WORK_DIR/init.dec
