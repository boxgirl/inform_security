import binascii

import operator

import math

import sys


def integer_byte_size(n):
	# get the number of bytes necessary to store the integer n
	quanta, mod = divmod(integer_bit_size(n), 8)
	if mod or n == 0:
		quanta += 1
	return quanta

def integer_bit_size(n):
	# get the number of bits necessary to store the integer n
	if n == 0:
		return 1
	s = 0
	while n:
		s += 1
		n >>= 1
	return s

def _pow(a, b, mod):

	return pow(a, b, mod)

def i2osp(x, x_len):
	# converts the integer x to its big-endian representation of length x_len
	if x > 256**x_len:
		raise Exception('Integer is too large')
	h = hex(x)[2:]
	if h[-1] == 'L':
		h = h[:-1]
	if len(h) & 1 == 1:
		h = '0%s' % h
	x = binascii.unhexlify(h)
	return b'\x00' * int(x_len-len(x)) + x

def os2ip(x):
	# converts the byte string x representing an integer reprented using the big-endian convient to an integer.

	h = binascii.hexlify(x)
	return int(h, 16)

def constant_time_cmp(a, b):
	# compare two strings using constant time
	result = True
	for x, y in zip(a,b):
		result &= (x == y)
	return result
