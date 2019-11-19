import struct
import numpy as np
from binascii import hexlify

# SHA-256
# len(hash): 32 bytes
# block size: 64 bytes
# word size: 4 bytes
# num of iterations: 64

# H(0)
# the fractional parts of the square roots of the first 8 primes (from 2 to 19)
H0 = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

# round constants
# the fractional parts of the cube roots of the first 64 primes (from 2 to 311)
K0 = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
		0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
		0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
		0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
		0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
		0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
		0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
		0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

def preprocessing(message):
	# round up
	m_length = len(message)
	blocks_num = (m_length + 1 + 8 + 63) // 64
	pad = blocks_num * 64 - m_length - 1 - 8
	# b'\x80' = '10000000' 
	message += b'\x80'
	message += b'\x00'*pad
	message += struct.pack('>Q', m_length * 8)

	return message

def split_to_blocks(message):

	return [message[i:i+64] for i in range(0,len(message),64)]

def hashing(message):

	if type(message) is list:

		message = b''.join([chr(i).encode() for i in message])

	else:

		message = message.encode()

	message = preprocessing(message)

	blocks = split_to_blocks(message)

	H = H0
	K = K0

	for block in blocks:

		words = [(struct.unpack(">I", block[i:i+4]))[0] for i in range(0,len(block),4)]

		# SHA-256 message schedule
		for i in range(16,64):
			words.append((sigma1(words[i-2]) + words[i-7] + sigma0(words[i-15]) + words[i-16]) & 0xFFFFFFFF)
		
		# init hash value for this block
		[a,b,c,d,e,f,g,h] = H

		for i in range(64):

			s0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
			maj = (a & b) ^ (a & c) ^ (b & c)
			t2 = (s0 + maj) & 0xFFFFFFFF
			s1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
			ch = (e & f) ^ ((0xFFFFFFFF^e) & g)
			t1 = (h + s1 + ch + K[i] + words[i]) & 0xFFFFFFFF
						
			h = g
			g = f
			f = e
			e = (d + t1) & 0xFFFFFFFF
			d = c
			c = b
			b = a
			a = (t1 + t2) & 0xFFFFFFFF

		H = np.add(H,[a,b,c,d,e,f,g,h])
		# cut for nedeed len (32)
		for j in range(len(H)):

			H[j] = H[j] & 0xFFFFFFFF

	dijest = b''.join([struct.pack('>I',h) for h in H])

	return dijest

# rotate right
def rotr(x, n):

	return ((x >> n) | (x << (32-n))) & 0xFFFFFFFF

# sigma 0
def sigma0(t):

	return (rotr(t, 7) ^ rotr(t, 18) ^ (t >> 3))

# sigma 1
def sigma1(t):

	return(rotr(t, 17) ^ rotr(t, 19) ^ (t >> 10))

if __name__=='__main__':

	message = ''
	res = hashing(message)
	print('Res: '+ hexlify(res).decode())
