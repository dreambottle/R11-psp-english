#!/bin/sh

# Generates xdelta3 patch files.
# Should be run after pack-afs.sh, requires xdelta3 on the PATH

XDELTA="xdelta3 -e -0 -f"
XDELTADIR="patches/xdelta3"
mkdir -p "${XDELTADIR}/mac"
BIPDIR="$XDELTADIR/../bip"
mkdir -p "${BIPDIR}/mac"

# set to "en" if unset
if [ -z "${TL_SUFFIX}" ]; then
    export TL_SUFFIX="en"
fi

# for i in r11_mac_${TL_SUFFIX}/*.BIP ; do
#     BASE=`basename $i .SCN`
#     cp -f r11_mac_${TL_SUFFIX}/${BASE}.BIP ${BIPDIR}/mac/${BASE}.BIP
# done

for i in r11_mac_${TL_SUFFIX}/*.SCN ; do
    BASE=`basename $i .SCN`
    echo xdelta3 $BASE

    # new simplified patch .bat just expects BIPs, old patch was expecting xdelta3 diffs for each decompressed BIP
    #$XDELTA -s r11_mac/${BASE}.SCN r11_mac_${TL_SUFFIX}/${BASE}.SCN $XDELTADIR/mac/${BASE}.SCN.xdelta3
    cp -f r11_mac_${TL_SUFFIX}/${BASE}.BIP ${BIPDIR}/mac/${BASE}.BIP
done

echo xdelta3 FONT00
$XDELTA -s r11_etc/FONT00.FNT r11_etc_${TL_SUFFIX}/FONT00.NEW $XDELTADIR/FONT00.FNT.xdelta3

echo xdelta3 init.bin
$XDELTA -s workdir/init.dec workdir/init.dec.${TL_SUFFIX} $XDELTADIR/init.dec.xdelta3

echo xdelta3 BOOT.BIN
# xdelta3 -e -9 -f -s workdir/BOOT.BIN workdir/BOOT.BIN.patched patches/xdelta3/BOOT.BIN.xdelta3
$XDELTA -s workdir/BOOT.BIN workdir/BOOT.BIN.${TL_SUFFIX} $XDELTADIR/BOOT.BIN.xdelta3

