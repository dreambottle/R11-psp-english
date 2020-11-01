#!/bin/bash
ISO_RES_DIR=r11_iso_extracted/PSP_GAME/USRDIR
ISO_BIN_DIR=r11_iso_extracted/PSP_GAME/SYSDIR
WORKDIR=./workdir
COMPRESS=./bin/compressbip
REPACK_AFS=./bin/repack_afs
REPACK_SCENE=text/repack_scene.py
ARMIPS=./tools/armips
if [ `uname` == "Darwin" ]; then
    ARMIPS=./tools/armips_osx
elif [ `uname` == "Linux" ]; then
    ARMIPS=./tools/armips_lin64
fi

# change this for other translations
# set to "en" if unset
if [ -z "${TL_SUFFIX}" ]; then
    export TL_SUFFIX="en"
fi

# Repack mac.afs (texts)
repack_mac_afs () {
	repack_scene () {
		$REPACK_SCENE text/tmp/mac-${TL_SUFFIX}-combined-psp/$1.txt r11_mac/$1.SCN r11_mac_${TL_SUFFIX}/$1.SCN
		$COMPRESS ./r11_mac_${TL_SUFFIX}/$1.{SCN,BIP}
	}

	mkdir -p r11_mac_${TL_SUFFIX}/
	
	# TODO cn
	./text/apply-shortcuts-translation.py text/other-psp-en/SHORTCUT.SCN.psp.txt r11_mac/SHORTCUT.SCN r11_mac_${TL_SUFFIX}/SHORTCUT.SCN || exit 1;
	$COMPRESS ./r11_mac_${TL_SUFFIX}/SHORTCUT.{SCN,BIP}
	
	for i in text/tmp/mac-${TL_SUFFIX}-combined-psp/*.txt ; do
		echo Repacking $i
		repack_scene `basename $i .txt` #& WAITPIDS="$! "$WAITPIDS
	done
	# wait $WAITPIDS &> /dev/null
	echo "Finished repacking scenes"

	$REPACK_AFS $WORKDIR/mac.afs $WORKDIR/mac-repacked.afs ./r11_mac_${TL_SUFFIX} || exit 1;
	mv -f $WORKDIR/mac-repacked.afs $ISO_RES_DIR/mac.afs
}

# Compose and repack font
# compose_font builds the font file 
compose_font () {
	mkdir -p r11_etc_${TL_SUFFIX}
	cd text/font/
	cp -f glyphs-new/* glyphs/
	if [ "cn" == "${TL_SUFFIX}" ]; then
		7z x glyphs-cn.7z
		mv -f glyphs-cn/* glyphs/
	fi
	python3 ../../py-src/extract_font.py repack glyphs/ || exit 1;
	cp FONT00.NEW ../../r11_etc_${TL_SUFFIX}/FONT00.NEW
	cd ../..
}

# repack_etc_afs repacks etc.afs with the new font file from "compose_font"
repack_etc_afs () {
	compose_font

	if [ -f r11_etc_${TL_SUFFIX}/FONT00.NEW ]; then
	$COMPRESS r11_etc_${TL_SUFFIX}/FONT00.NEW r11_etc_${TL_SUFFIX}/FONT00.FOP
	$REPACK_AFS $WORKDIR/etc.afs $WORKDIR/etc-repacked.afs r11_etc_${TL_SUFFIX} || exit 1;
	mv -f $WORKDIR/etc-repacked.afs $ISO_RES_DIR/etc.afs
	fi
}

# Repack init.bin
repack_init_bin () {
	# Apply init.bin strings
	./py-src/apply_init_translation.py text/other-psp-${TL_SUFFIX}/init.bin.utf8.txt workdir/init.dec workdir/init.dec.${TL_SUFFIX} ${TL_SUFFIX} || exit 1;

	INIT_SRC=$WORKDIR/init.dec.${TL_SUFFIX}
	if [ ! -f $INIT_SRC ]; then
		# If modified file does not exist, just repack the original one.
		# Used for testing purposes
		INIT_SRC=$WORKDIR/init.dec
	fi
	echo "Compressing $INIT_SRC"
	$COMPRESS $INIT_SRC $WORKDIR/init.${TL_SUFFIX}.bin || exit 1;
	mv -f $WORKDIR/init.${TL_SUFFIX}.bin $ISO_RES_DIR/init.bin
}

# Patch BOOT.BIN
patch_boot_bin () {
	# Apply translation
	./py-src/apply_boot_translation.py text/other-psp-${TL_SUFFIX}/BOOT.utf8.txt workdir/BOOT.BIN workdir/BOOT.BIN.${TL_SUFFIX} ${TL_SUFFIX} || exit 1;

	echo "Applying patches to BOOT.BIN"
	mv -f $WORKDIR/BOOT.BIN.${TL_SUFFIX} $WORKDIR/BOOT.BIN.patched
	if [ "cn" == "${TL_SUFFIX}" ]; then
		$ARMIPS src/boot-patches-cn.asm -root workdir/ || exit 1;
	else
		$ARMIPS src/boot-patches.asm -root workdir/ || exit 1;
	fi
	rm -f $ISO_BIN_DIR/BOOT.BIN
	rm -f $ISO_BIN_DIR/EBOOT.BIN
	cp -f $WORKDIR/BOOT.BIN.patched ./$ISO_BIN_DIR/EBOOT.BIN
	mv -f $WORKDIR/BOOT.BIN.patched ./$ISO_BIN_DIR/BOOT.BIN
}

# Actually running above functions
repack_mac_afs
repack_etc_afs
repack_init_bin
patch_boot_bin
