#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct, wave, array
from soundprocess.consts import *

def bytestr_to_numeric(data, frames, samp_width, channels, endian = None):
	if channels == 1:
		return struct.unpack('%c%d%c' % ('' if endian is None else ENDIAN[endian], frames, PFM[samp_width]), data)


def numeric_to_bytestr(data, samp_width, channels):
	# write endian ...
	if channels == 1:
		return array.array('%c' % PFM[samp_width], data).tostring()


def read_wav(name):
	'''指定したwavファイルの波形および詳細の取得
	name 	--- 対象ファイル名
	戻り値:
		wavファイルの情報(Tuple)，wavを格納したlist
	例外:
		モノラルや8，16bitサンプリング以外は未対応
	'''
	wav =  wave.open(name)
	if not wav.getnchannels() == 1:
		wav.close()
		raise Exception('NotSupportChannel, Must mono')
	sampwidth = wav.getsampwidth()
	if not (sampwidth == 1 or sampwidth == 2):
		wav.close()
		raise Exception('NotSupportSampwidth, Must 8 or 16bit')
	data = bytestr_to_numeric(wav.readframes(wav.getnframes()), wav.getnframes(), wav.getsampwidth(), wav.getnchannels())

	'''
	# for Stereo
	buf = wav.readframes(wav.getnframes())
	if sampwidth == 1:
		channel_1 = [struct.unpack('%c' % (PFM[wav.getsampwidth()]), i) for i in buf[::2]]
		channel_2 = [struct.unpack('%c' % (PFM[wav.getsampwidth()]), i) for i in buf[1::2]]
	else if sampwidth == 2:
		channel_1 = [struct.unpack('%c' % (PFM[wav.getsampwidth()]), i+j) for (i,j) in zip(buf[::4], buf[1::4])]
		channel_2 = [struct.unpack('%c' % (PFM[wav.getsampwidth()]), i+j) for (i,j) in zip(buf[2::4], buf[3::4])]
	'''
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


def read_raw(name, endian, sampwidth, channels, endian):
	f = open(name, 'rb')
	buf = f.read()
	f.close()
	frames = len(buf) / (sampwidth * channels)

	return bytestr_to_numeric(buf, frames, sampwidth, channels, endian)

