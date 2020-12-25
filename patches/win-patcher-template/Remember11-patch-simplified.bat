@echo off


echo 1. Extracting files from the iso image.
rmdir /s /q iso_extracted >nul 2>&1
bin-win32\7z.exe x Remember11-jap.iso -o"iso_extracted"

rmdir /s /q tmp >nul 2>&1
mkdir tmp\

echo 2. Repacking mac.afs (Main game text)
bin-win32\repack_afs.exe iso_extracted\PSP_GAME\USRDIR\mac.afs tmp\mac.afs bip\mac\ >nul

echo 3. Patching etc.afs (Font)
bin-win32\repack_afs.exe iso_extracted\PSP_GAME\USRDIR\etc.afs tmp\etc.afs.jp nul tmp\etc >nul 2>&1
bin-win32\decompressbip.exe tmp\etc\FONT00.FOP tmp\etc\FONT00.FNT >nul
mkdir tmp\etc-en\
bin-win32\xdelta3.exe -f -d -s tmp\etc\FONT00.FNT xdelta3\FONT00.FNT.xdelta3 tmp\etc-en\FONT00.FNT
bin-win32\compressbip.exe tmp\etc-en\FONT00.FNT tmp\etc-en\FONT00.FOP >nul
bin-win32\repack_afs.exe iso_extracted\PSP_GAME\USRDIR\etc.afs tmp\etc.afs tmp\etc-en >nul

echo 4. Patching init.bin (TIPS and misc. text)
bin-win32\decompressbip.exe iso_extracted\PSP_GAME\USRDIR\init.bin tmp\init.dec >nul
bin-win32\xdelta3.exe -f -d -s tmp\init.dec xdelta3\init.dec.xdelta3 tmp\init.dec.en
bin-win32\compressbip.exe tmp\init.dec.en tmp\init.bin >nul

echo 5. Patching BOOT.BIN (Menu text and assembly patches)
bin-win32\xdelta3.exe -f -d -s iso_extracted\PSP_GAME\SYSDIR\BOOT.BIN xdelta3\BOOT.BIN.xdelta3 tmp\BOOT.BIN

echo 6. Creating a new iso image.
copy /Y tmp\BOOT.BIN iso_extracted\PSP_GAME\SYSDIR\EBOOT.BIN >nul
move /Y tmp\BOOT.BIN iso_extracted\PSP_GAME\SYSDIR\BOOT.BIN >nul
move /Y tmp\init.bin iso_extracted\PSP_GAME\USRDIR\init.bin >nul
move /Y tmp\mac.afs iso_extracted\PSP_GAME\USRDIR\mac.afs >nul
move /Y tmp\etc.afs iso_extracted\PSP_GAME\USRDIR\etc.afs >nul

bin-win32\mkisofs.exe -quiet -iso-level 4 -xa -A "PSP GAME" -V "R11" -sysid "PSP GAME" -volset "" -p "" -publisher "" -o Remember11-patched.iso iso_extracted

echo Deleting temp files.
rmdir /s /q iso_extracted
rmdir /s /q tmp
echo Remember11 ISO successfully patched!
@pause
