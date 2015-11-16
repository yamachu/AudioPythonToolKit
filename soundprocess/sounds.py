#!/usr/bin/env python
# -*- coding: utf-8 -*-
import soundprocess.utils as utils
import os


class Sounds():
	__sampwitdh = 2
	__framerate = 16000
	__nchannels = 1
	__comptype = 'NONE'
	__compname = 'not compressed'

	"""docstring for Sounds"""
	def __init__(self, 
		sampwidth = __sampwitdh, framerate = __framerate, channels = __nchannels,
		comptype = __comptype, compname = __compname, data = None):
		self.sampwidth = sampwidth
		self.framerate = framerate
		self.nchannels = channels
		self.comptype = comptype
		self.compname = compname
		self.data = data
		if data is not None:
			self.frames = len(data) / channels


	@classmethod
	def init_from_file(cls, name, endian = 'l', sampwidth = __sampwitdh,
		framerate = __framerate, channels = __nchannels):
		'''Get Sounds instanse from file
		read non header sound file that suffix is not wav or wave,
		must set parameters
		name --- filename
		endian --- 'l': little endian, 'b': big endian, default: l
		sampwidth --- bit depth (8bit->1, 16bit->2), default: 2
		framerate --- default: 16000
		channels --- default: 1
		'''
		filename_withsuffix = os.path.basename(name)
		filename = os.path.splitext(filename_withsuffix)[0]
		suffix = os.path.splitext(filename_withsuffix)[1]

		if suffix == '.wav' or suffix == '.wave':
			try:
				info, data = utils.read_wav(name)
			except Exception as exc:
				raise exc
			else:
				return cls(data = data, channels = info[0], sampwidth = info[1],
					framerate = info[2], comptype = info[4], compname = info[5])
		else:
			data = utils.read_raw(name, endian, sampwidth, channels, endian)
			return cls(cls, data = data, channels = channels, sampwidth = sampwidth,
					framerate = framerate)
