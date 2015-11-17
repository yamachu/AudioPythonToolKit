#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct, wave, array
from soundprocess.consts import *

def bytestr_to_numeric(data, frames, sampwidth, channels, file_endian = None):
	if file_endian is None:
		return struct.unpack('%d%c' % (frames * channels, PFM[sampwidth]), data)
	else:
		return struct.unpack('%c%d%c' % (ENDIAN[file_endian], frames * channels, PFM[sampwidth]), data)


def numeric_to_bytestr(data, sampwidth, file_endian = None):
	return array.array('%c' % PFM[sampwidth], data).tostring()


def read_wav(name):
	'''指定したwavファイルの波形および詳細の取得
	name 	--- 対象ファイル名
	戻り値:
		wavファイルの情報(Tuple)，wavを格納したlist
	例外:
		8，16bitサンプリング以外は未対応
	'''
	wav =  wave.open(name)
	sampwidth = wav.getsampwidth()
	if not (sampwidth == 1 or sampwidth == 2):
		wav.close()
		raise Exception('NotSupportSampwidth, Must 8 or 16bit')
	data = bytestr_to_numeric(wav.readframes(wav.getnframes()), wav.getnframes(), wav.getsampwidth(), wav.getnchannels())
	info = wav.getparams()
	wav.close()
	return (info, data)


def write_wav(name, buf, param):
	'''指定したパラメータでwavファイルに出力
	name 	--- 出力ファイル名
	buf 	--- 8，16ビットの配列
	param 	--- wavファイルの情報
	'''
	data = numeric_to_bytestr(buf, param[1], param[0])
	w = wave.open(name, 'wb')
	w.setparams(param)
	w.writeframes(data)
	w.close()


def read_raw(name, sampwidth, channels, file_endian):
	f = open(name, 'rb')
	buf = f.read()
	f.close()
	frames = len(buf) / (sampwidth * channels)

	return bytestr_to_numeric(buf, frames, sampwidth, channels, file_endian)


def write_raw(name, data, sampwidth, file_endian):
	buf = numeric_to_bytestr(data, sampwidth, file_endian)

	f = open(name, 'wb')
	f.write(buf)
	f.close()

