@echo off


echo 1. Extracting files from the iso image.
rmdir /s /q iso_extracted >nul 2>&1
bin-win32\7z.exe x Remember11-jap.iso -o"iso_extracted"

rmdir /s /q tmp >nul 2>&1
mkdir tmp\
mkdir tmp\mac-en\

echo 2. Patching Scene Texts.
echo - Unpacking mac.afs.
bin-win32\repack_afs.exe iso_extracted\PSP_GAME\USRDIR\mac.afs tmp\mac.afs.jp nul tmp\mac >nul 2>&1


echo - Patching scene files.

bin-win32\decompressbip.exe tmp\mac\CO1_01.BIP tmp\mac\CO1_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_01.SCN xdelta3\mac\CO1_01.SCN.xdelta3 tmp\mac-en\CO1_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_01.SCN tmp\mac-en\CO1_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_02.BIP tmp\mac\CO1_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_02.SCN xdelta3\mac\CO1_02.SCN.xdelta3 tmp\mac-en\CO1_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_02.SCN tmp\mac-en\CO1_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_03.BIP tmp\mac\CO1_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_03.SCN xdelta3\mac\CO1_03.SCN.xdelta3 tmp\mac-en\CO1_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_03.SCN tmp\mac-en\CO1_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_04.BIP tmp\mac\CO1_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_04.SCN xdelta3\mac\CO1_04.SCN.xdelta3 tmp\mac-en\CO1_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_04.SCN tmp\mac-en\CO1_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_05.BIP tmp\mac\CO1_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_05.SCN xdelta3\mac\CO1_05.SCN.xdelta3 tmp\mac-en\CO1_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_05.SCN tmp\mac-en\CO1_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_06.BIP tmp\mac\CO1_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_06.SCN xdelta3\mac\CO1_06.SCN.xdelta3 tmp\mac-en\CO1_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_06.SCN tmp\mac-en\CO1_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_07.BIP tmp\mac\CO1_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_07.SCN xdelta3\mac\CO1_07.SCN.xdelta3 tmp\mac-en\CO1_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_07.SCN tmp\mac-en\CO1_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_08.BIP tmp\mac\CO1_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_08.SCN xdelta3\mac\CO1_08.SCN.xdelta3 tmp\mac-en\CO1_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_08.SCN tmp\mac-en\CO1_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_09.BIP tmp\mac\CO1_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_09.SCN xdelta3\mac\CO1_09.SCN.xdelta3 tmp\mac-en\CO1_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_09.SCN tmp\mac-en\CO1_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_10.BIP tmp\mac\CO1_10.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_10.SCN xdelta3\mac\CO1_10.SCN.xdelta3 tmp\mac-en\CO1_10.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_10.SCN tmp\mac-en\CO1_10.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_11.BIP tmp\mac\CO1_11.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_11.SCN xdelta3\mac\CO1_11.SCN.xdelta3 tmp\mac-en\CO1_11.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_11.SCN tmp\mac-en\CO1_11.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_12.BIP tmp\mac\CO1_12.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_12.SCN xdelta3\mac\CO1_12.SCN.xdelta3 tmp\mac-en\CO1_12.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_12.SCN tmp\mac-en\CO1_12.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO1_13.BIP tmp\mac\CO1_13.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO1_13.SCN xdelta3\mac\CO1_13.SCN.xdelta3 tmp\mac-en\CO1_13.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO1_13.SCN tmp\mac-en\CO1_13.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_01.BIP tmp\mac\CO2_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_01.SCN xdelta3\mac\CO2_01.SCN.xdelta3 tmp\mac-en\CO2_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_01.SCN tmp\mac-en\CO2_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_02.BIP tmp\mac\CO2_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_02.SCN xdelta3\mac\CO2_02.SCN.xdelta3 tmp\mac-en\CO2_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_02.SCN tmp\mac-en\CO2_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_03.BIP tmp\mac\CO2_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_03.SCN xdelta3\mac\CO2_03.SCN.xdelta3 tmp\mac-en\CO2_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_03.SCN tmp\mac-en\CO2_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_04.BIP tmp\mac\CO2_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_04.SCN xdelta3\mac\CO2_04.SCN.xdelta3 tmp\mac-en\CO2_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_04.SCN tmp\mac-en\CO2_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_05.BIP tmp\mac\CO2_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_05.SCN xdelta3\mac\CO2_05.SCN.xdelta3 tmp\mac-en\CO2_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_05.SCN tmp\mac-en\CO2_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_06.BIP tmp\mac\CO2_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_06.SCN xdelta3\mac\CO2_06.SCN.xdelta3 tmp\mac-en\CO2_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_06.SCN tmp\mac-en\CO2_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_07.BIP tmp\mac\CO2_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_07.SCN xdelta3\mac\CO2_07.SCN.xdelta3 tmp\mac-en\CO2_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_07.SCN tmp\mac-en\CO2_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_08.BIP tmp\mac\CO2_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_08.SCN xdelta3\mac\CO2_08.SCN.xdelta3 tmp\mac-en\CO2_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_08.SCN tmp\mac-en\CO2_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_09A.BIP tmp\mac\CO2_09A.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_09A.SCN xdelta3\mac\CO2_09A.SCN.xdelta3 tmp\mac-en\CO2_09A.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_09A.SCN tmp\mac-en\CO2_09A.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_09B.BIP tmp\mac\CO2_09B.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_09B.SCN xdelta3\mac\CO2_09B.SCN.xdelta3 tmp\mac-en\CO2_09B.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_09B.SCN tmp\mac-en\CO2_09B.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_10.BIP tmp\mac\CO2_10.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_10.SCN xdelta3\mac\CO2_10.SCN.xdelta3 tmp\mac-en\CO2_10.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_10.SCN tmp\mac-en\CO2_10.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_11.BIP tmp\mac\CO2_11.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_11.SCN xdelta3\mac\CO2_11.SCN.xdelta3 tmp\mac-en\CO2_11.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_11.SCN tmp\mac-en\CO2_11.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO2_12.BIP tmp\mac\CO2_12.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO2_12.SCN xdelta3\mac\CO2_12.SCN.xdelta3 tmp\mac-en\CO2_12.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO2_12.SCN tmp\mac-en\CO2_12.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_01.BIP tmp\mac\CO3_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_01.SCN xdelta3\mac\CO3_01.SCN.xdelta3 tmp\mac-en\CO3_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_01.SCN tmp\mac-en\CO3_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_02.BIP tmp\mac\CO3_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_02.SCN xdelta3\mac\CO3_02.SCN.xdelta3 tmp\mac-en\CO3_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_02.SCN tmp\mac-en\CO3_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_03.BIP tmp\mac\CO3_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_03.SCN xdelta3\mac\CO3_03.SCN.xdelta3 tmp\mac-en\CO3_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_03.SCN tmp\mac-en\CO3_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_04.BIP tmp\mac\CO3_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_04.SCN xdelta3\mac\CO3_04.SCN.xdelta3 tmp\mac-en\CO3_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_04.SCN tmp\mac-en\CO3_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_05.BIP tmp\mac\CO3_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_05.SCN xdelta3\mac\CO3_05.SCN.xdelta3 tmp\mac-en\CO3_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_05.SCN tmp\mac-en\CO3_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_06.BIP tmp\mac\CO3_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_06.SCN xdelta3\mac\CO3_06.SCN.xdelta3 tmp\mac-en\CO3_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_06.SCN tmp\mac-en\CO3_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_07.BIP tmp\mac\CO3_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_07.SCN xdelta3\mac\CO3_07.SCN.xdelta3 tmp\mac-en\CO3_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_07.SCN tmp\mac-en\CO3_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_08.BIP tmp\mac\CO3_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_08.SCN xdelta3\mac\CO3_08.SCN.xdelta3 tmp\mac-en\CO3_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_08.SCN tmp\mac-en\CO3_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_09.BIP tmp\mac\CO3_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_09.SCN xdelta3\mac\CO3_09.SCN.xdelta3 tmp\mac-en\CO3_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_09.SCN tmp\mac-en\CO3_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO3_10.BIP tmp\mac\CO3_10.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO3_10.SCN xdelta3\mac\CO3_10.SCN.xdelta3 tmp\mac-en\CO3_10.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO3_10.SCN tmp\mac-en\CO3_10.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO4_01.BIP tmp\mac\CO4_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_01.SCN xdelta3\mac\CO4_01.SCN.xdelta3 tmp\mac-en\CO4_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_01.SCN tmp\mac-en\CO4_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO4_02.BIP tmp\mac\CO4_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_02.SCN xdelta3\mac\CO4_02.SCN.xdelta3 tmp\mac-en\CO4_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_02.SCN tmp\mac-en\CO4_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO4_03.BIP tmp\mac\CO4_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_03.SCN xdelta3\mac\CO4_03.SCN.xdelta3 tmp\mac-en\CO4_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_03.SCN tmp\mac-en\CO4_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO4_04.BIP tmp\mac\CO4_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_04.SCN xdelta3\mac\CO4_04.SCN.xdelta3 tmp\mac-en\CO4_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_04.SCN tmp\mac-en\CO4_04.BIP >nul

echo -- 25%% patched...

bin-win32\decompressbip.exe tmp\mac\CO4_05.BIP tmp\mac\CO4_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_05.SCN xdelta3\mac\CO4_05.SCN.xdelta3 tmp\mac-en\CO4_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_05.SCN tmp\mac-en\CO4_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO4_06.BIP tmp\mac\CO4_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_06.SCN xdelta3\mac\CO4_06.SCN.xdelta3 tmp\mac-en\CO4_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_06.SCN tmp\mac-en\CO4_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO4_07.BIP tmp\mac\CO4_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_07.SCN xdelta3\mac\CO4_07.SCN.xdelta3 tmp\mac-en\CO4_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_07.SCN tmp\mac-en\CO4_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO4_08.BIP tmp\mac\CO4_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_08.SCN xdelta3\mac\CO4_08.SCN.xdelta3 tmp\mac-en\CO4_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_08.SCN tmp\mac-en\CO4_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO4_09.BIP tmp\mac\CO4_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO4_09.SCN xdelta3\mac\CO4_09.SCN.xdelta3 tmp\mac-en\CO4_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO4_09.SCN tmp\mac-en\CO4_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_01.BIP tmp\mac\CO5_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_01.SCN xdelta3\mac\CO5_01.SCN.xdelta3 tmp\mac-en\CO5_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_01.SCN tmp\mac-en\CO5_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_02.BIP tmp\mac\CO5_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_02.SCN xdelta3\mac\CO5_02.SCN.xdelta3 tmp\mac-en\CO5_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_02.SCN tmp\mac-en\CO5_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_03.BIP tmp\mac\CO5_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_03.SCN xdelta3\mac\CO5_03.SCN.xdelta3 tmp\mac-en\CO5_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_03.SCN tmp\mac-en\CO5_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_04.BIP tmp\mac\CO5_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_04.SCN xdelta3\mac\CO5_04.SCN.xdelta3 tmp\mac-en\CO5_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_04.SCN tmp\mac-en\CO5_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_05.BIP tmp\mac\CO5_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_05.SCN xdelta3\mac\CO5_05.SCN.xdelta3 tmp\mac-en\CO5_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_05.SCN tmp\mac-en\CO5_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_06.BIP tmp\mac\CO5_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_06.SCN xdelta3\mac\CO5_06.SCN.xdelta3 tmp\mac-en\CO5_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_06.SCN tmp\mac-en\CO5_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_07.BIP tmp\mac\CO5_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_07.SCN xdelta3\mac\CO5_07.SCN.xdelta3 tmp\mac-en\CO5_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_07.SCN tmp\mac-en\CO5_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_08.BIP tmp\mac\CO5_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_08.SCN xdelta3\mac\CO5_08.SCN.xdelta3 tmp\mac-en\CO5_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_08.SCN tmp\mac-en\CO5_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_09.BIP tmp\mac\CO5_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_09.SCN xdelta3\mac\CO5_09.SCN.xdelta3 tmp\mac-en\CO5_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_09.SCN tmp\mac-en\CO5_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_10.BIP tmp\mac\CO5_10.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_10.SCN xdelta3\mac\CO5_10.SCN.xdelta3 tmp\mac-en\CO5_10.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_10.SCN tmp\mac-en\CO5_10.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_11.BIP tmp\mac\CO5_11.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_11.SCN xdelta3\mac\CO5_11.SCN.xdelta3 tmp\mac-en\CO5_11.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_11.SCN tmp\mac-en\CO5_11.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_12.BIP tmp\mac\CO5_12.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_12.SCN xdelta3\mac\CO5_12.SCN.xdelta3 tmp\mac-en\CO5_12.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_12.SCN tmp\mac-en\CO5_12.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO5_13.BIP tmp\mac\CO5_13.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO5_13.SCN xdelta3\mac\CO5_13.SCN.xdelta3 tmp\mac-en\CO5_13.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO5_13.SCN tmp\mac-en\CO5_13.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO6_01.BIP tmp\mac\CO6_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO6_01.SCN xdelta3\mac\CO6_01.SCN.xdelta3 tmp\mac-en\CO6_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO6_01.SCN tmp\mac-en\CO6_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO6_02.BIP tmp\mac\CO6_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO6_02.SCN xdelta3\mac\CO6_02.SCN.xdelta3 tmp\mac-en\CO6_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO6_02.SCN tmp\mac-en\CO6_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO6_03.BIP tmp\mac\CO6_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO6_03.SCN xdelta3\mac\CO6_03.SCN.xdelta3 tmp\mac-en\CO6_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO6_03.SCN tmp\mac-en\CO6_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO6_04.BIP tmp\mac\CO6_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO6_04.SCN xdelta3\mac\CO6_04.SCN.xdelta3 tmp\mac-en\CO6_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO6_04.SCN tmp\mac-en\CO6_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO6_05.BIP tmp\mac\CO6_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO6_05.SCN xdelta3\mac\CO6_05.SCN.xdelta3 tmp\mac-en\CO6_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO6_05.SCN tmp\mac-en\CO6_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO7_01.BIP tmp\mac\CO7_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO7_01.SCN xdelta3\mac\CO7_01.SCN.xdelta3 tmp\mac-en\CO7_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO7_01.SCN tmp\mac-en\CO7_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO7_02.BIP tmp\mac\CO7_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO7_02.SCN xdelta3\mac\CO7_02.SCN.xdelta3 tmp\mac-en\CO7_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO7_02.SCN tmp\mac-en\CO7_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO7_03.BIP tmp\mac\CO7_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO7_03.SCN xdelta3\mac\CO7_03.SCN.xdelta3 tmp\mac-en\CO7_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO7_03.SCN tmp\mac-en\CO7_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO7_04.BIP tmp\mac\CO7_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO7_04.SCN xdelta3\mac\CO7_04.SCN.xdelta3 tmp\mac-en\CO7_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO7_04.SCN tmp\mac-en\CO7_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO7_05.BIP tmp\mac\CO7_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO7_05.SCN xdelta3\mac\CO7_05.SCN.xdelta3 tmp\mac-en\CO7_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO7_05.SCN tmp\mac-en\CO7_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO7_06.BIP tmp\mac\CO7_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO7_06.SCN xdelta3\mac\CO7_06.SCN.xdelta3 tmp\mac-en\CO7_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO7_06.SCN tmp\mac-en\CO7_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\CO7_07.BIP tmp\mac\CO7_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\CO7_07.SCN xdelta3\mac\CO7_07.SCN.xdelta3 tmp\mac-en\CO7_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\CO7_07.SCN tmp\mac-en\CO7_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\COEP_01.BIP tmp\mac\COEP_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\COEP_01.SCN xdelta3\mac\COEP_01.SCN.xdelta3 tmp\mac-en\COEP_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\COEP_01.SCN tmp\mac-en\COEP_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\PR_01.BIP tmp\mac\PR_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\PR_01.SCN xdelta3\mac\PR_01.SCN.xdelta3 tmp\mac-en\PR_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\PR_01.SCN tmp\mac-en\PR_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\PR_02.BIP tmp\mac\PR_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\PR_02.SCN xdelta3\mac\PR_02.SCN.xdelta3 tmp\mac-en\PR_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\PR_02.SCN tmp\mac-en\PR_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\PR_03.BIP tmp\mac\PR_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\PR_03.SCN xdelta3\mac\PR_03.SCN.xdelta3 tmp\mac-en\PR_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\PR_03.SCN tmp\mac-en\PR_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA1_01.BIP tmp\mac\SA1_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_01.SCN xdelta3\mac\SA1_01.SCN.xdelta3 tmp\mac-en\SA1_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_01.SCN tmp\mac-en\SA1_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA1_02.BIP tmp\mac\SA1_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_02.SCN xdelta3\mac\SA1_02.SCN.xdelta3 tmp\mac-en\SA1_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_02.SCN tmp\mac-en\SA1_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA1_03.BIP tmp\mac\SA1_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_03.SCN xdelta3\mac\SA1_03.SCN.xdelta3 tmp\mac-en\SA1_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_03.SCN tmp\mac-en\SA1_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA1_04.BIP tmp\mac\SA1_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_04.SCN xdelta3\mac\SA1_04.SCN.xdelta3 tmp\mac-en\SA1_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_04.SCN tmp\mac-en\SA1_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA1_05.BIP tmp\mac\SA1_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_05.SCN xdelta3\mac\SA1_05.SCN.xdelta3 tmp\mac-en\SA1_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_05.SCN tmp\mac-en\SA1_05.BIP >nul

echo -- 50%% patched...

bin-win32\decompressbip.exe tmp\mac\SA1_06.BIP tmp\mac\SA1_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_06.SCN xdelta3\mac\SA1_06.SCN.xdelta3 tmp\mac-en\SA1_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_06.SCN tmp\mac-en\SA1_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA1_07.BIP tmp\mac\SA1_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_07.SCN xdelta3\mac\SA1_07.SCN.xdelta3 tmp\mac-en\SA1_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_07.SCN tmp\mac-en\SA1_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA1_08.BIP tmp\mac\SA1_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_08.SCN xdelta3\mac\SA1_08.SCN.xdelta3 tmp\mac-en\SA1_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_08.SCN tmp\mac-en\SA1_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA1_09.BIP tmp\mac\SA1_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA1_09.SCN xdelta3\mac\SA1_09.SCN.xdelta3 tmp\mac-en\SA1_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA1_09.SCN tmp\mac-en\SA1_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_01.BIP tmp\mac\SA2_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_01.SCN xdelta3\mac\SA2_01.SCN.xdelta3 tmp\mac-en\SA2_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_01.SCN tmp\mac-en\SA2_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_02.BIP tmp\mac\SA2_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_02.SCN xdelta3\mac\SA2_02.SCN.xdelta3 tmp\mac-en\SA2_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_02.SCN tmp\mac-en\SA2_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_03.BIP tmp\mac\SA2_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_03.SCN xdelta3\mac\SA2_03.SCN.xdelta3 tmp\mac-en\SA2_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_03.SCN tmp\mac-en\SA2_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_04.BIP tmp\mac\SA2_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_04.SCN xdelta3\mac\SA2_04.SCN.xdelta3 tmp\mac-en\SA2_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_04.SCN tmp\mac-en\SA2_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_05.BIP tmp\mac\SA2_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_05.SCN xdelta3\mac\SA2_05.SCN.xdelta3 tmp\mac-en\SA2_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_05.SCN tmp\mac-en\SA2_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_06.BIP tmp\mac\SA2_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_06.SCN xdelta3\mac\SA2_06.SCN.xdelta3 tmp\mac-en\SA2_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_06.SCN tmp\mac-en\SA2_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_07.BIP tmp\mac\SA2_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_07.SCN xdelta3\mac\SA2_07.SCN.xdelta3 tmp\mac-en\SA2_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_07.SCN tmp\mac-en\SA2_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_08.BIP tmp\mac\SA2_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_08.SCN xdelta3\mac\SA2_08.SCN.xdelta3 tmp\mac-en\SA2_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_08.SCN tmp\mac-en\SA2_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_09.BIP tmp\mac\SA2_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_09.SCN xdelta3\mac\SA2_09.SCN.xdelta3 tmp\mac-en\SA2_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_09.SCN tmp\mac-en\SA2_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_10.BIP tmp\mac\SA2_10.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_10.SCN xdelta3\mac\SA2_10.SCN.xdelta3 tmp\mac-en\SA2_10.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_10.SCN tmp\mac-en\SA2_10.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_11.BIP tmp\mac\SA2_11.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_11.SCN xdelta3\mac\SA2_11.SCN.xdelta3 tmp\mac-en\SA2_11.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_11.SCN tmp\mac-en\SA2_11.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_12.BIP tmp\mac\SA2_12.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_12.SCN xdelta3\mac\SA2_12.SCN.xdelta3 tmp\mac-en\SA2_12.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_12.SCN tmp\mac-en\SA2_12.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_13.BIP tmp\mac\SA2_13.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_13.SCN xdelta3\mac\SA2_13.SCN.xdelta3 tmp\mac-en\SA2_13.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_13.SCN tmp\mac-en\SA2_13.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_14.BIP tmp\mac\SA2_14.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_14.SCN xdelta3\mac\SA2_14.SCN.xdelta3 tmp\mac-en\SA2_14.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_14.SCN tmp\mac-en\SA2_14.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA2_15.BIP tmp\mac\SA2_15.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA2_15.SCN xdelta3\mac\SA2_15.SCN.xdelta3 tmp\mac-en\SA2_15.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA2_15.SCN tmp\mac-en\SA2_15.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_01.BIP tmp\mac\SA3_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_01.SCN xdelta3\mac\SA3_01.SCN.xdelta3 tmp\mac-en\SA3_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_01.SCN tmp\mac-en\SA3_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_02.BIP tmp\mac\SA3_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_02.SCN xdelta3\mac\SA3_02.SCN.xdelta3 tmp\mac-en\SA3_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_02.SCN tmp\mac-en\SA3_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_03.BIP tmp\mac\SA3_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_03.SCN xdelta3\mac\SA3_03.SCN.xdelta3 tmp\mac-en\SA3_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_03.SCN tmp\mac-en\SA3_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_04.BIP tmp\mac\SA3_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_04.SCN xdelta3\mac\SA3_04.SCN.xdelta3 tmp\mac-en\SA3_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_04.SCN tmp\mac-en\SA3_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_05.BIP tmp\mac\SA3_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_05.SCN xdelta3\mac\SA3_05.SCN.xdelta3 tmp\mac-en\SA3_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_05.SCN tmp\mac-en\SA3_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_06.BIP tmp\mac\SA3_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_06.SCN xdelta3\mac\SA3_06.SCN.xdelta3 tmp\mac-en\SA3_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_06.SCN tmp\mac-en\SA3_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_07.BIP tmp\mac\SA3_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_07.SCN xdelta3\mac\SA3_07.SCN.xdelta3 tmp\mac-en\SA3_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_07.SCN tmp\mac-en\SA3_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_08.BIP tmp\mac\SA3_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_08.SCN xdelta3\mac\SA3_08.SCN.xdelta3 tmp\mac-en\SA3_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_08.SCN tmp\mac-en\SA3_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_09.BIP tmp\mac\SA3_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_09.SCN xdelta3\mac\SA3_09.SCN.xdelta3 tmp\mac-en\SA3_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_09.SCN tmp\mac-en\SA3_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_10.BIP tmp\mac\SA3_10.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_10.SCN xdelta3\mac\SA3_10.SCN.xdelta3 tmp\mac-en\SA3_10.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_10.SCN tmp\mac-en\SA3_10.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_11.BIP tmp\mac\SA3_11.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_11.SCN xdelta3\mac\SA3_11.SCN.xdelta3 tmp\mac-en\SA3_11.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_11.SCN tmp\mac-en\SA3_11.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_12.BIP tmp\mac\SA3_12.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_12.SCN xdelta3\mac\SA3_12.SCN.xdelta3 tmp\mac-en\SA3_12.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_12.SCN tmp\mac-en\SA3_12.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_13.BIP tmp\mac\SA3_13.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_13.SCN xdelta3\mac\SA3_13.SCN.xdelta3 tmp\mac-en\SA3_13.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_13.SCN tmp\mac-en\SA3_13.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_14.BIP tmp\mac\SA3_14.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_14.SCN xdelta3\mac\SA3_14.SCN.xdelta3 tmp\mac-en\SA3_14.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_14.SCN tmp\mac-en\SA3_14.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA3_15.BIP tmp\mac\SA3_15.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA3_15.SCN xdelta3\mac\SA3_15.SCN.xdelta3 tmp\mac-en\SA3_15.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA3_15.SCN tmp\mac-en\SA3_15.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_01.BIP tmp\mac\SA4_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_01.SCN xdelta3\mac\SA4_01.SCN.xdelta3 tmp\mac-en\SA4_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_01.SCN tmp\mac-en\SA4_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_02.BIP tmp\mac\SA4_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_02.SCN xdelta3\mac\SA4_02.SCN.xdelta3 tmp\mac-en\SA4_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_02.SCN tmp\mac-en\SA4_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_03.BIP tmp\mac\SA4_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_03.SCN xdelta3\mac\SA4_03.SCN.xdelta3 tmp\mac-en\SA4_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_03.SCN tmp\mac-en\SA4_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_04.BIP tmp\mac\SA4_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_04.SCN xdelta3\mac\SA4_04.SCN.xdelta3 tmp\mac-en\SA4_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_04.SCN tmp\mac-en\SA4_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_05.BIP tmp\mac\SA4_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_05.SCN xdelta3\mac\SA4_05.SCN.xdelta3 tmp\mac-en\SA4_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_05.SCN tmp\mac-en\SA4_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_06.BIP tmp\mac\SA4_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_06.SCN xdelta3\mac\SA4_06.SCN.xdelta3 tmp\mac-en\SA4_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_06.SCN tmp\mac-en\SA4_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_07.BIP tmp\mac\SA4_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_07.SCN xdelta3\mac\SA4_07.SCN.xdelta3 tmp\mac-en\SA4_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_07.SCN tmp\mac-en\SA4_07.BIP >nul

echo -- 75%% patched...

bin-win32\decompressbip.exe tmp\mac\SA4_08.BIP tmp\mac\SA4_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_08.SCN xdelta3\mac\SA4_08.SCN.xdelta3 tmp\mac-en\SA4_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_08.SCN tmp\mac-en\SA4_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_09.BIP tmp\mac\SA4_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_09.SCN xdelta3\mac\SA4_09.SCN.xdelta3 tmp\mac-en\SA4_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_09.SCN tmp\mac-en\SA4_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_10.BIP tmp\mac\SA4_10.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_10.SCN xdelta3\mac\SA4_10.SCN.xdelta3 tmp\mac-en\SA4_10.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_10.SCN tmp\mac-en\SA4_10.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_11.BIP tmp\mac\SA4_11.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_11.SCN xdelta3\mac\SA4_11.SCN.xdelta3 tmp\mac-en\SA4_11.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_11.SCN tmp\mac-en\SA4_11.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_12.BIP tmp\mac\SA4_12.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_12.SCN xdelta3\mac\SA4_12.SCN.xdelta3 tmp\mac-en\SA4_12.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_12.SCN tmp\mac-en\SA4_12.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA4_13.BIP tmp\mac\SA4_13.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA4_13.SCN xdelta3\mac\SA4_13.SCN.xdelta3 tmp\mac-en\SA4_13.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA4_13.SCN tmp\mac-en\SA4_13.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_01.BIP tmp\mac\SA5_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_01.SCN xdelta3\mac\SA5_01.SCN.xdelta3 tmp\mac-en\SA5_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_01.SCN tmp\mac-en\SA5_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_02.BIP tmp\mac\SA5_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_02.SCN xdelta3\mac\SA5_02.SCN.xdelta3 tmp\mac-en\SA5_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_02.SCN tmp\mac-en\SA5_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_03.BIP tmp\mac\SA5_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_03.SCN xdelta3\mac\SA5_03.SCN.xdelta3 tmp\mac-en\SA5_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_03.SCN tmp\mac-en\SA5_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_04.BIP tmp\mac\SA5_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_04.SCN xdelta3\mac\SA5_04.SCN.xdelta3 tmp\mac-en\SA5_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_04.SCN tmp\mac-en\SA5_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_05.BIP tmp\mac\SA5_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_05.SCN xdelta3\mac\SA5_05.SCN.xdelta3 tmp\mac-en\SA5_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_05.SCN tmp\mac-en\SA5_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_06.BIP tmp\mac\SA5_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_06.SCN xdelta3\mac\SA5_06.SCN.xdelta3 tmp\mac-en\SA5_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_06.SCN tmp\mac-en\SA5_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_07.BIP tmp\mac\SA5_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_07.SCN xdelta3\mac\SA5_07.SCN.xdelta3 tmp\mac-en\SA5_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_07.SCN tmp\mac-en\SA5_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_08.BIP tmp\mac\SA5_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_08.SCN xdelta3\mac\SA5_08.SCN.xdelta3 tmp\mac-en\SA5_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_08.SCN tmp\mac-en\SA5_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA5_09.BIP tmp\mac\SA5_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA5_09.SCN xdelta3\mac\SA5_09.SCN.xdelta3 tmp\mac-en\SA5_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA5_09.SCN tmp\mac-en\SA5_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA6_01.BIP tmp\mac\SA6_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA6_01.SCN xdelta3\mac\SA6_01.SCN.xdelta3 tmp\mac-en\SA6_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA6_01.SCN tmp\mac-en\SA6_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA6_02.BIP tmp\mac\SA6_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA6_02.SCN xdelta3\mac\SA6_02.SCN.xdelta3 tmp\mac-en\SA6_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA6_02.SCN tmp\mac-en\SA6_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA6_03.BIP tmp\mac\SA6_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA6_03.SCN xdelta3\mac\SA6_03.SCN.xdelta3 tmp\mac-en\SA6_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA6_03.SCN tmp\mac-en\SA6_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA6_04.BIP tmp\mac\SA6_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA6_04.SCN xdelta3\mac\SA6_04.SCN.xdelta3 tmp\mac-en\SA6_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA6_04.SCN tmp\mac-en\SA6_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA6_05.BIP tmp\mac\SA6_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA6_05.SCN xdelta3\mac\SA6_05.SCN.xdelta3 tmp\mac-en\SA6_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA6_05.SCN tmp\mac-en\SA6_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_01.BIP tmp\mac\SA7_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_01.SCN xdelta3\mac\SA7_01.SCN.xdelta3 tmp\mac-en\SA7_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_01.SCN tmp\mac-en\SA7_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_02.BIP tmp\mac\SA7_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_02.SCN xdelta3\mac\SA7_02.SCN.xdelta3 tmp\mac-en\SA7_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_02.SCN tmp\mac-en\SA7_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_03.BIP tmp\mac\SA7_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_03.SCN xdelta3\mac\SA7_03.SCN.xdelta3 tmp\mac-en\SA7_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_03.SCN tmp\mac-en\SA7_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_04.BIP tmp\mac\SA7_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_04.SCN xdelta3\mac\SA7_04.SCN.xdelta3 tmp\mac-en\SA7_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_04.SCN tmp\mac-en\SA7_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_05.BIP tmp\mac\SA7_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_05.SCN xdelta3\mac\SA7_05.SCN.xdelta3 tmp\mac-en\SA7_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_05.SCN tmp\mac-en\SA7_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_06.BIP tmp\mac\SA7_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_06.SCN xdelta3\mac\SA7_06.SCN.xdelta3 tmp\mac-en\SA7_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_06.SCN tmp\mac-en\SA7_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_07.BIP tmp\mac\SA7_07.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_07.SCN xdelta3\mac\SA7_07.SCN.xdelta3 tmp\mac-en\SA7_07.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_07.SCN tmp\mac-en\SA7_07.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_08.BIP tmp\mac\SA7_08.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_08.SCN xdelta3\mac\SA7_08.SCN.xdelta3 tmp\mac-en\SA7_08.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_08.SCN tmp\mac-en\SA7_08.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SA7_09.BIP tmp\mac\SA7_09.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SA7_09.SCN xdelta3\mac\SA7_09.SCN.xdelta3 tmp\mac-en\SA7_09.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SA7_09.SCN tmp\mac-en\SA7_09.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SAEP_01.BIP tmp\mac\SAEP_01.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SAEP_01.SCN xdelta3\mac\SAEP_01.SCN.xdelta3 tmp\mac-en\SAEP_01.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SAEP_01.SCN tmp\mac-en\SAEP_01.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SAEP_02.BIP tmp\mac\SAEP_02.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SAEP_02.SCN xdelta3\mac\SAEP_02.SCN.xdelta3 tmp\mac-en\SAEP_02.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SAEP_02.SCN tmp\mac-en\SAEP_02.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SAEP_03.BIP tmp\mac\SAEP_03.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SAEP_03.SCN xdelta3\mac\SAEP_03.SCN.xdelta3 tmp\mac-en\SAEP_03.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SAEP_03.SCN tmp\mac-en\SAEP_03.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SAEP_04.BIP tmp\mac\SAEP_04.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SAEP_04.SCN xdelta3\mac\SAEP_04.SCN.xdelta3 tmp\mac-en\SAEP_04.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SAEP_04.SCN tmp\mac-en\SAEP_04.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SAEP_05.BIP tmp\mac\SAEP_05.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SAEP_05.SCN xdelta3\mac\SAEP_05.SCN.xdelta3 tmp\mac-en\SAEP_05.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SAEP_05.SCN tmp\mac-en\SAEP_05.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SAEP_06.BIP tmp\mac\SAEP_06.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SAEP_06.SCN xdelta3\mac\SAEP_06.SCN.xdelta3 tmp\mac-en\SAEP_06.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SAEP_06.SCN tmp\mac-en\SAEP_06.BIP >nul

bin-win32\decompressbip.exe tmp\mac\SHORTCUT.BIP tmp\mac\SHORTCUT.SCN >nul
bin-win32\xdelta3.exe -f -d -s tmp\mac\SHORTCUT.SCN xdelta3\mac\SHORTCUT.SCN.xdelta3 tmp\mac-en\SHORTCUT.SCN >nul
bin-win32\compressbip.exe tmp\mac-en\SHORTCUT.SCN tmp\mac-en\SHORTCUT.BIP >nul

echo -- Done.
echo - Repacking mac.afs with patched scene files.

bin-win32\repack_afs.exe iso_extracted\PSP_GAME\USRDIR\mac.afs tmp\mac.afs tmp\mac-en >nul

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

echo 5. Patching BOOT.BIN (Menu text and asembly patches)
bin-win32\xdelta3.exe -f -d -s iso_extracted\PSP_GAME\SYSDIR\BOOT.BIN xdelta3\BOOT.BIN.xdelta3 tmp\BOOT.BIN

echo 6. Creating a new iso image.
copy /Y tmp\BOOT.BIN iso_extracted\PSP_GAME\SYSDIR\EBOOT.BIN >nul
move /Y tmp\BOOT.BIN iso_extracted\PSP_GAME\SYSDIR\BOOT.BIN >nul
move /Y tmp\init.bin iso_extracted\PSP_GAME\USRDIR\init.bin >nul
move /Y tmp\mac.afs iso_extracted\PSP_GAME\USRDIR\mac.afs >nul
move /Y tmp\etc.afs iso_extracted\PSP_GAME\USRDIR\etc.afs >nul

bin-win32\mkisofs.exe -quiet -iso-level 4 -xa -A "PSP GAME" -V "R11" -sysid "PSP GAME" -volset "" -p "" -publisher "" -o Remember11-eng-v2.0.iso iso_extracted

echo Deleting temp files.
rmdir /s /q iso_extracted
rmdir /s /q tmp
echo Remember11 ISO successfully patched!
@pause
