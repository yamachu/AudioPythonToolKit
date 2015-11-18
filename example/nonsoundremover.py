#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, argparse
sys.path.append(os.pardir)
from soundprocess.calc import *
from soundprocess.sounds import *
from soundprocess.media import *

# CONST VALS
LEAVE_TIME = 5
REMOVE_DB = -60

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
		フレーム番号(ないなら0)
	'''
	for (i, x) in enumerate(data[::-1]):
		if x > amp:
			return i
	else:
		return 0


if __name__ == '__main__':
	common_parser = argparse.ArgumentParser()
	common_parser.add_argument('-e', '--end_margin', type=float, nargs='?', const=LEAVE_TIME, default=LEAVE_TIME)
	common_parser.add_argument('-l', '--lower_db', type=float, nargs='?', const=REMOVE_DB, default=REMOVE_DB)
	common_parser.add_argument('--outplotdir', nargs='?', default=None)
	common_parser.add_argument('--endian', choices=['l','b'], nargs='?')
	common_parser.add_argument('-c', '--channels', type=int, choices=[1,2], nargs='?')
	common_parser.add_argument('-f', '--freq', type=int, nargs='?')
	common_parser.add_argument('--sampwidth', type=int, nargs='?', choices=[1,2])

	sub_parsers = common_parser.add_subparsers(dest='subparser_name')

	single_parser = sub_parsers.add_parser('single')
	single_parser.add_argument('input')
	single_parser.add_argument('output')
	single_parser.add_argument('--showplot', action='store_true')
	
	multi_parser = sub_parsers.add_parser('multi')
	multi_parser.add_argument('--outdir', required=True)
	multi_parser.add_argument('inputs', nargs='+')
	
	args = common_parser.parse_args()

	limit_amp = convert_db_to_amp(args.lower_db)
	leave_time = args.end_margin

	if args.subparser_name == 'single':
		inputs = [args.input]
	else:
		inputs = args.inputs

	for i_file in inputs:
		filename_withsuffix = os.path.basename(i_file)
		filename = os.path.splitext(filename_withsuffix)[0]
		suffix = os.path.splitext(filename_withsuffix)[1]
		# info -> (channel, sampwidth, framerate, frames, ...)
		try:
			if suffix == '.wav':
				snd = Sounds.init_from_file(i_file)
			else:
				snd = Sounds.init_from_file(i_file, sampwidth = args.sampwidth, framerate = args.freq, channels = args.channels, endian = args.endian)
		except Exception as exc:
			print 'Readfile Exception: %s' % i_file
			print exc
			continue
		else:
			limit_idx_from_last = get_index_of_remove_start_from_last(snd.data, limit_amp)
			remove_idx_from_last = get_remove_frame_from_last_with_leave_time(
				leave_time, limit_idx_from_last, snd.framerate)
			proccess_data_buf = snd.data[:int(snd.frames - remove_idx_from_last)]

			outparam = snd.get_info()

			outsnd = Sounds(*outparam, data = proccess_data_buf)

			outplotdir = None
			if args.subparser_name == 'single':
				outname = args.output
			else:
				outname = os.path.join(args.outdir,filename_withsuffix)
			if not hasattr(args, 'showplot'):
				showflg = False
			else:
				showflg = args.showplot
			if showflg is True or args.outplotdir is not None:
				wav_plotting(proccess_data_buf, snd.framerate, snd.sampwidth, filename, showflg, args.outplotdir)
			outsnd.write_to_file(outname)

