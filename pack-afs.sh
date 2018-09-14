#!/bin/bash
ISO_RES_DIR=iso_extracted/PSP_GAME/USRDIR
ISO_BIN_DIR=iso_extracted/PSP_GAME/SYSDIR
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


# Repack mac.afs (texts)
repack_mac_afs () {
	repack_scene () {
		$REPACK_SCENE text/mac-combined-psp/$1.txt mac/$1.SCN mac-en/$1.SCN
		$COMPRESS ./mac-en/$1.{SCN,BIP}
	}

	mkdir -p mac-en/
	
	./text/apply-shortcuts-translation.py text/other-psp/SHORTCUT.SCN.psp.txt mac/SHORTCUT.SCN mac-en/SHORTCUT.SCN || exit 1;
	$COMPRESS ./mac-en/SHORTCUT.{SCN,BIP}
	
	for i in text/mac-combined-psp/*.txt ; do
		echo Repacking $i
		repack_scene `basename $i .txt` #& WAITPIDS="$! "$WAITPIDS
	done
	# wait $WAITPIDS &> /dev/null
	echo "Finished repacking scenes"

	$REPACK_AFS $WORKDIR/mac.afs $WORKDIR/mac-repacked.afs ./mac-en || exit 1;
	mv -f $WORKDIR/mac-repacked.afs $ISO_RES_DIR/mac.afs
}

# Compose and repack font
# compose_font builds the font file 
compose_font () {
	mkdir -p etc-en
	cd text/font
	cp -f glyphs-new/* glyphs/
	python3 extract-font.py repack glyphs/ || exit 1;
	cp FONT00.NEW ../../etc-en/FONT00.NEW
	cd ../..
}

# repack_etc_afs repacks etc.afs with the new font file from "compose_font"
repack_etc_afs () {
	compose_font

	if [ -f etc-en/FONT00.NEW ]; then
	$COMPRESS etc-en/FONT00.NEW etc-en/FONT00.FOP
	$REPACK_AFS $WORKDIR/etc.afs $WORKDIR/etc-repacked.afs etc-en || exit 1;
	mv -f $WORKDIR/etc-repacked.afs $ISO_RES_DIR/etc.afs
	fi
}

# Repack init.bin
repack_init_bin () {
	# Apply init.bin strings
	./text/apply-init-translation.py text/other-psp/init.psp.txt workdir/init.dec workdir/init.dec.en || exit 1;

	INIT_SRC=$WORKDIR/init.dec.en
	if [ ! -f $INIT_SRC ]; then
		# If modified file does not exist, just repack the original one.
		# Used for testing purposes
		INIT_SRC=$WORKDIR/init.dec
	fi
	echo "Compressing $INIT_SRC"
	$COMPRESS $INIT_SRC $WORKDIR/init.en.bin || exit 1;
	mv -f $WORKDIR/init.en.bin $ISO_RES_DIR/init.bin
}

# Patch BOOT.BIN
patch_boot_bin () {
	# Apply translation
	./text/apply-boot-translation.py text/other-psp/BOOT.BIN.psp.txt workdir/BOOT.BIN workdir/BOOT.BIN.en || exit 1;

	echo "Applying patches to BOOT.BIN"
	cp -f $WORKDIR/BOOT.BIN.en $WORKDIR/BOOT.BIN.patched
	$ARMIPS src/boot-patches.asm -root workdir/ || exit 1;
	rm -f $ISO_BIN_DIR/BOOT.BIN
	rm -f $ISO_BIN_DIR/EBOOT.BIN
	cp -f $WORKDIR/BOOT.BIN.patched ./$ISO_BIN_DIR/EBOOT.BIN
	cp -f $WORKDIR/BOOT.BIN.patched ./$ISO_BIN_DIR/BOOT.BIN
}

# Actually running above functions
repack_mac_afs
repack_etc_afs
repack_init_bin
patch_boot_bin
