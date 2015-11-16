#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.pardir)
from soundprocess.calc import *
from soundprocess.utils import *
from soundprocess.media import *

# CONST VALS
LEAVE_TIME = 5
REMOVE_DB = -60

__doc__ = """
Non sound remover.
Usage:
	{f} <input> <output> [--noout] [-e END_MARGIN | --end_margin END_MARGIN] [--lower_db=<LOW_DB>] [--showplot] [--outplotdir=<outplotdir>]
	{f} multi --outdir=<outdir> [-e END_MARGIN | --end_margin END_MARGIN] [--lower_db=<LOW_DB>] [--noout] [--outplotdir=<outplotdir>]　<input>... 
	{f} (-h | --help)

Options:
	-e END_MARGIN --end_margin END_MARGIN 	Leave non sound time(ms) [default: {lt}]
	--lower_db=<LOW_DB>						Remove sound less than LOW_DB [default: {rd}]
	following are not impleented...
	--noout 								Set this flag, show result but don't write file
	--showplot
	--outdir=<outdir>
	--outplotdir

Example:
	{f} src.wav out.wav -e 10 --lower_db=-50 # margin is 10ms, limit dB is -50dB
	{f} src.wav out.wav --end_margin 10 --lower_db=-50 # it's same

Notice:
	If you input non-wavfile(.raw, .dat, etc...), 
	MUST set sampFreq, bitDepth, channel.
""".format(f=__file__, lt=LEAVE_TIME, rd=REMOVE_DB)


def get_remove_frame_from_last_with_leave_time(leave, limit_idx, samp_freq):
	'''末尾からの指定した削除マージンを含めたフレームを取得
	leave 	--- 残したい秒数
	limit_idx 	--- 制限値を越したフレーム
	samp_freq 	--- サンプリング周波数
	戻り値:
		マージンを含めた削除フレーム(マージン未満の場合0)
	'''
	samp_interval = 1.0 / samp_freq
	leave_time_to_frame = leave / 1000.0 / samp_interval
	diff =  limit_idx - leave_time_to_frame
	return diff if diff > 0 else 0


def get_index_of_remove_start_from_last(data, amp):
	'''指定した振幅よりも大きくなるフレームを末尾から取得
	data 	--- wavを格納したlist
	amp 	--- 制限値
	戻り値:
		成功:　フレーム番号，失敗:　0
	'''
	for (i, x) in enumerate(data[::-1]):
		if x > amp:
			return i
	else:
		return 0


if __name__ == '__main__':
	from docopt import docopt
	import os

	args = docopt(__doc__)
	print args

	limit_amp = convert_db_to_amp(REMOVE_DB if args['--lower_db'] is None else float(args['--lower_db']))
	leave_time = LEAVE_TIME if args['END_MARGIN'] is None else float(args['END_MARGIN'])
		
	for i_file in args['<input>']:
		filename_withsuffix = os.path.basename(i_file)
		filename = os.path.splitext(filename_withsuffix)[0]
		suffix = os.path.splitext(filename_withsuffix)[1]
		print filename_withsuffix
		print filename
		print suffix
		# info -> (channel, sampwidth, framerate, frames, ...)
		# data -> [0fra, 1fra, 2fra ...] (type is signed char(integer) or signed short)
		try:
			if suffix == '.wav':
				info, data = read_wav(i_file)
		except Exception as exc:
			print 'Readfile Exception: %s' % i_file
			print exc
			continue
		else:
			# liner search... bad algorism
			limit_idx_from_last = get_index_of_remove_start_from_last(data, limit_amp)
			remove_idx_from_last = get_remove_frame_from_last_with_leave_time(
				leave_time, limit_idx_from_last, info[2])
			proccess_data_buf = data[:int(len(data) - remove_idx_from_last)]

			outparam = (info[0], info[1], info[2], len(proccess_data_buf), info[4], info[5])

			outplotdir = None
			outname = args['<output>'] if not args['<output>'] is None else filename_withsuffix
			if not args['--outdir'] is None:
				outname = os.path.join(args['--outdir'],outname)
			if not (args['--showplot'] == False and args['--outplotdir'] is None):
				if not args['--noout']:
					outplotdir = args['--outplotdir']
				wav_plotting(proccess_data_buf, info[2], info[1], filename, args['--showplot'], outplotdir)
			if not args['--noout']:
				write_wav(outname, proccess_data_buf, outparam)

'''
ToDo:
	Support multi channel sound
	Byte order...support? (big endian and little endian)
	Support non wav file (.raw, .dat, etc...)
	24 bit sound...support????
	wave info and form marge into single class
'''