import numpy as np
from binascii import hexlify

# sha-3
# 24 rounds
# 5*5 - states' mtx with words of len 64 bits => 1600 bits
# working part of state - rate, else - capacity

def bytes_to_word64(partial_m):

	return sum((partial_m[i] << (8 * i)) for i in range(8))

def words64_to_bytes(word):

	return list((word >> (8 * i)) % 256 for i in range(8))

def rotation(el, offset):

	 return ((el >> (64 - (offset % 64))) + (el << (offset % 64))) % (1 << 64)

def keccak_1600(state):

	# init matrix 5*5 with element like words64
	A = [[0 for j in range(5)] for i in range(5)]

	for i in range(5):

		for j in range(5):

			k = 8 * (i + 5 * j)
			A[i][j] = bytes_to_word64(state[k : k + 8])

	R = 1

	for round_ in range(24):
		# 1 step 

		# contains 5 words64
		C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
		D = [C[(x - 1) % 5] ^ rotation(C[(x + 1) % 5], 1) for x in range(5)]

		A = [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]

		x, y, current = 1, 0, A[1][0]

		# 2 and 3 steps
		for t in range(24):

			x, y = y, (2 * x + 3 * y) % 5
			offset = ((t + 1) * (t + 2)) // 2
			current, A[x][y] = A[x][y], rotation(current, offset)

		# 4 step
		for y in range(5):

			B = [A[x][y] for x in range(5)]

			for x in range(5):

				A[x][y] = B[x] ^ ((~B[(x + 1) % 5]) & B[(x + 2) % 5])

		# 5 step 
		# break the symmetry of the rounds
		for j in range(7):

			R = ((R << 1) ^ ((R >> 7) * 0x71)) % 256

			if R & 2: 

				A[0][0] ^= 1 << ((1 << j) - 1)

	for x in range(5):

		for y in range(5):
			
			i = 8 * (x + 5 * y)
			state[i : i + 8] = words64_to_bytes(A[x][y])

	return state

def process(message, size, suffix=0x06):

	rate = (1600 - size * 2)//8
	c = (size * 2)//8
	output_len = size//8


	length_m = len(message)

	if type(message) is str:

		message = [ord(i) for i in message]

	state = bytearray(rate + c)
	# pad10*1 - rule
	block, offset = 0, 0

	# absorbing
	while offset < length_m:

		block = min(length_m - offset, rate)

		for i in range(block):
			# sum mod 2
			state[i] ^= message[i + offset]

		offset += block

		if block == rate:

			state = keccak_1600(state)
			block = 0

	# padding
	state[block] ^= suffix
	# b'\x80' = '10000000' 
	if (suffix & 0x80) and (block == (rate - 1)):

		state = keccak_1600(state)

	state[rate - 1] ^= 0x80

	state = keccak_1600(state)

	# squeezing
	output = bytearray()

	while output_len:

		block = min(output_len, rate)
		output += state[:block]
		output_len -= block

		if output_len:

			state = keccak_1600(state)

	return output

if __name__=='__main__':

	message = 'The quick brown fox jumps over the lazy dog'
	size = 384
	res = process(message, size)
	print('Res: '+ hexlify(res).decode())
