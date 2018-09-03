#!/bin/sh

# Generates xdelta3 patch files.
# Should be run after pack-afs.sh.

XDELTA="xdelta3 -e -0 -f"

XDELTADIR="patches/xdelta3"
mkdir -p "${XDELTADIR}/mac"

for i in mac-en/*.SCN ; do
    BASE=`basename $i .SCN`
    echo xdelta3 $BASE
    $XDELTA -s mac/${BASE}.SCN mac-en/${BASE}.SCN $XDELTADIR/mac/${BASE}.SCN.xdelta3
done

echo xdelta3 FONT00
$XDELTA -s etc/FONT00.FNT etc-en/FONT00.NEW $XDELTADIR/FONT00.FNT.xdelta3

echo xdelta3 init.bin
$XDELTA -s workdir/init.dec workdir/init.dec.en $XDELTADIR/init.dec.xdelta3

echo xdelta3 BOOT.BIN
# xdelta3 -e -9 -f -s workdir/BOOT.BIN workdir/BOOT.BIN.patched patches/xdelta3/BOOT.BIN.xdelta3
$XDELTA -s workdir/BOOT.BIN workdir/BOOT.BIN.patched $XDELTADIR/BOOT.BIN.xdelta3

