#こちら参考に。https://twitter.com/boyahina/status/1346041627949731842/
#             https://twitter.com/bakueikozo/status/1347204355582173184
#JPEG FORMAT https://www.setsuki.com/hsp/ext/jpg.htm
#WAV FORMAT https://www.youfit.co.jp/archives/1418
import  sys
import os

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
if data[0:4] != b'SAVI':
    print('マジョカアイリス動画ファイルではありません')
    exit()

#WAV取り出し 0x14-0x17
#MediaPlayerでは鳴りませんでした。MPC-HCで鳴りました。
wavDataStart = int.from_bytes(data[0x14:0x17], byteorder='little') 
wavDataSize =  int.from_bytes(data[wavDataStart + 4:wavDataStart + 8], byteorder='little') + 8
print("wavStart=" + hex(wavDataStart) + ":size=" + hex(wavDataSize))
wavFileName = baseFileName + '.wav'
wavFile = open(wavFileName, 'wb')
wavFile.write(data[wavDataStart:wavDataStart + wavDataSize])
wavFile.close()

#JPEG取り出し

#JPEG画像枚数 0x10-0x13 ヘッダ分を引いてます
jpegCount = int.from_bytes(data[0x10:0x13], byteorder='little') - 1

#JPEGヘッダ開始 0x28-0x2B
jpegHeaderDataStart = int.from_bytes(data[0x28:0x2B], byteorder='little')
#JPEGヘッダサイズ 0x2C-0x2F
jpegHeaderDataSize = int.from_bytes(data[0x2C:0x2F], byteorder='little')

jpegHeader = data[jpegHeaderDataStart:jpegHeaderDataStart + jpegHeaderDataSize]

print("JpegCount=" + str(jpegCount))

#JPEG画像開始 0x20-0x23
jpegIndexStart = int.from_bytes(data[0x20:0x23], byteorder='little') 

index = 1
while index < jpegCount:
    jpegIndexEnd = jpegIndexStart + 4
    jpegDataStart = int.from_bytes(data[jpegIndexStart:jpegIndexEnd], byteorder='little')
    jpegDataEnd = int.from_bytes(data[jpegIndexEnd:(jpegIndexEnd+4)], byteorder='little')
    print(str(index) + ":indexStart=" + hex(jpegIndexStart) + ": jpegStart=" + hex(jpegDataStart) + ": jpegEnd=" + hex(jpegDataEnd))

    if jpegDataStart < jpegDataEnd:
        jpegFileName = baseFileName + '_' + str(index) + '.jpg'
        jpegFile = open(jpegFileName, 'wb')
        #ヘッダ + データで出力
        jpegFile.write(jpegHeader + data[jpegDataStart:jpegDataEnd])
        jpegFile.close()
        index = index + 1
    else:
        print("data skip")
    jpegIndexStart = jpegIndexEnd
    
