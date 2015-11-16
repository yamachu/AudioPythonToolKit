#!/usr/bin/env python
# -*- coding: utf-8 -*-
from soundprocess.consts import *

def convert_db_to_amp(db, bit_depth = 2):
	'''指定したdBに対する振幅を返す
	db 	--- 求めたい振幅に対応するdB(負数)
	bit_depth 	--- ビット深度(デフォルト値は2 -> 16bit)
	戻り値:
		振幅
	'''
	return pow(10.0, db / 20.0) * SNB[bit_depth]