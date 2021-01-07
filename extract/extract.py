#こちら参考に。https://twitter.com/boyahina/status/1346041627949731842/photo/1
#JPEG FORMAT https://www.setsuki.com/hsp/ext/jpg.htm
#WAV FORMAT https://www.youfit.co.jp/archives/1418
import  sys
import os
import struct

args = sys.argv
if len(args) != 2:
    quit();

sourceFileName = args[1]

baseFileName = sourceFileName.split(".")[0]

movieFile = open(sourceFileName, 'rb')

#全部読む
data = movieFile.read()
movieFile.close()

#ヘッダ確認
if data[0:3] != b'SAV':
    print('マジョカアイリス動画ファイルではありません')
    exit()

#WAV取り出し 0x14
#WAV 抽出してみたけど鳴らないですね…。
wavDataStart = int.from_bytes(data[0x14:0x17], byteorder='little') 
wavDataSize =  int.from_bytes(data[wavDataStart + 4:wavDataStart + 8], byteorder='little') + 8
print("wavStart=" + hex(wavDataStart) + ":size=" + hex(wavDataSize))
wavFileName = baseFileName + '.wav'
wavFile = open(wavFileName, 'wb')
wavFile.write(data[wavDataStart:wavDataStart + wavDataSize])
wavFile.close()

#JPEG取り出し
#まだいまのところ、うまく取り出せたり取り出せなかったりします。
#画像枚数 0x10
jpegCount = int.from_bytes(data[0x10:0x13], byteorder='little') - 1

#jpegIndex位置ひとまず決め打ち
jpegIndexStart = 0x28
header = b''
for index in range(jpegCount):
    jpegIndexEnd = jpegIndexStart + 4
    jpegDataStart = int.from_bytes(data[jpegIndexStart:jpegIndexEnd], byteorder='little')
    jpegDataEnd = int.from_bytes(data[jpegIndexEnd:(jpegIndexEnd+4)], byteorder='little')
    print(str(index) + ":indexStart=" + hex(jpegIndexStart) + ": jpegStart=" + hex(jpegDataStart) + ": jpegEnd=" + hex(jpegDataEnd))

    if jpegDataStart > jpegDataEnd:
        print("データエラー？")
        jpegIndexStart = jpegIndexEnd
        continue

    #FFDAが出てくるまではヘッダ
    if data[jpegDataStart+1] != 0xda:
        header = header + data[jpegDataStart:jpegDataEnd]
        print("header")
    else:
        jpegFileName = baseFileName + '_' + str(index) + '.jpg'
        jpegFile = open(jpegFileName, 'wb')
        #ヘッダ + データで出力
        jpegFile.write(header + data[jpegDataStart:jpegDataEnd])
        jpegFile.close()
        print("data")
    jpegIndexStart = jpegIndexEnd


