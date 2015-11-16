#!/usr/bin/env python
# -*- coding: utf-8 -*-
from soundprocess.consts import *

def wav_plotting(data, samp_freq, samp_width, name = None, show = False, save_dir = None):
	import pylab
	samp_interval = 1.0 / samp_freq
	times = [i * samp_interval for i in xrange(len(data))]
	pylab.plot(times, data)
	pylab.title(name if not name is None else 'Waveform')
	pylab.xlabel('Time[s]')
	pylab.ylabel('Amplitude')
	pylab.xlim([0,  times[len(data) - 1]])
	pylab.ylim([-SNB[samp_width], SNB[samp_width] - 1])
	if not save_dir is None:
		import os
		save_name = 'plot.png' if name is None else name + '.png'
		save_name = os.path.join(save_dir,save_name)
		pylab.savefig(save_name)
	if show:
		pylab.show()