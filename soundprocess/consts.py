#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''共通定数集
'''

# signed :null bit, 8bit, 16bit, 24bit
SNB = [0, 128, 32768, 8388608]
# Pack format
PFM = [None, 'b', 'h', None]
# Pack endian
ENDIAN = {'l': '<', 'b': '>'}