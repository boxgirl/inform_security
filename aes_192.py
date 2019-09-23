from copy import copy

sbox = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]

isbox = [82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]

Rcon = [0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141]

Nb = 4					# num of columns, default value
Nk = 6					# len of key in 32-bit words, 192/32 = 6
Nr = 12					# num of rounds, default value


# encryption block

def encryption(block, w):

	state = add_round_key(block, w[:Nb])

	for r in range(1, Nr):

		state = sub_bytes(state)
		state = shift_rows(state)
		state = mix_columns(state)
		state = add_round_key(state, w[r*Nb:(r+1)*Nb])

	state = sub_bytes(state)
	state = shift_rows(state)
	state = add_round_key(state, w[Nr*Nb:(Nr+1)*Nb])

	return state

def sub_word(word):

	return [sbox[i] for i in word]


def sub_bytes(state):

	return [sub_word(i) for i in state]


def shift_rows(state):

	matrix = [word[:] for word in state]

	for i in range(Nb):

		for j in range(Nb):

			matrix[i][j] = state[(i+j) % Nb][j]

	return matrix


# Galois Multiplication

def galois_mult(a, b):

	p = 0
	hiBitSet = 0

	for i in range(8):

		if b & 1 == 1:

			p ^= a

		hiBitSet = a & 0x80
		a <<= 1

		if hiBitSet == 0x80:

			a ^= 0x1b

		b >>= 1

	return p % 256

def mix_column(column):

	temp = copy(column)
	column[0] = galois_mult(temp[0],2) ^ galois_mult(temp[3],1) ^ \
				galois_mult(temp[2],1) ^ galois_mult(temp[1],3)
	column[1] = galois_mult(temp[1],2) ^ galois_mult(temp[0],1) ^ \
				galois_mult(temp[3],1) ^ galois_mult(temp[2],3)
	column[2] = galois_mult(temp[2],2) ^ galois_mult(temp[1],1) ^ \
				galois_mult(temp[0],1) ^ galois_mult(temp[3],3)
	column[3] = galois_mult(temp[3],2) ^ galois_mult(temp[2],1) ^ \
				galois_mult(temp[1],1) ^ galois_mult(temp[0],3)

def mix_columns(state):

	for i in range(4):

		column = []

		for j in range(4):

			column.append(state[i][j])

		mix_column(column)

		# transfer the new values back into the state table
		for j in range(4):

			state[i][j] = column[j]

	return state

def key_expansion(key):

	# get key_schedule: table with Nb * (Nr + 1) columns, or (Nr + 1) blocks

	key = prepare_key(key)

	w = [word[:] for word in key]

	i = Nk

	while i < Nb * (Nr + 1):

		# i - number of column
		temp = w[i-1][:]
		# first column in each block
		if i % Nk == 0:

			temp = sub_word(rot_word(temp))
			temp[0] ^= Rcon[(i//Nk)]

		for j in range(len(temp)):

			# XOR el of Wi column in i-block with Wi column in i-1 block
			temp[j] ^= w[i-Nk][j]

		w.append(temp[:])
		# go to next column 
		i += 1

	return w


def rot_word(word):

	return word[1:] + word[0:1]


def prepare_key(key):

	# transforme list key to matrix

	matrix = []
	word = []

	for i, b in enumerate(key):

		word.append(b)

		if i % 4 == 3:

			matrix.append(word)
			word = []

	return matrix

# decryption block

def decryption(block, w):

	state = add_round_key(block, w[Nr*Nb:(Nr+1)*Nb])

	for r in range(Nr-1, 0, -1):

		state = inv_shift_rows(state)
		state = inv_sub_bytes(state)
		state = add_round_key(state, w[r*Nb:(r+1)*Nb])
		state = inv_mix_columns(state)

	state = inv_shift_rows(state)
	state = inv_sub_bytes(state)
	state = add_round_key(state, w[:Nb])

	return state


def inv_sub_bytes(state):

	return [[isbox[byte] for byte in word] for word in state]


def inv_shift_rows(state):

	matrix = [word[:] for word in state]

	for i in range(Nb):

		for j in range(Nb):

			matrix[i][j] = state[(i-j) % Nb][j]

	return matrix


def inv_mix_column(column):

	temp = copy(column)
	column[0] = galois_mult(temp[0],14) ^ galois_mult(temp[3],9) ^ \
				galois_mult(temp[2],13) ^ galois_mult(temp[1],11)
	column[1] = galois_mult(temp[1],14) ^ galois_mult(temp[0],9) ^ \
				galois_mult(temp[3],13) ^ galois_mult(temp[2],11)
	column[2] = galois_mult(temp[2],14) ^ galois_mult(temp[1],9) ^ \
				galois_mult(temp[0],13) ^ galois_mult(temp[3],11)
	column[3] = galois_mult(temp[3],14) ^ galois_mult(temp[2],9) ^ \
				galois_mult(temp[1],13) ^ galois_mult(temp[0],11)

def inv_mix_columns(state):
	for i in range(Nb):
		column = []
		for j in range(Nb):
			column.append(state[i][j])
		inv_mix_column(column)
		for j in range(Nb):
			state[i][j] = column[j]
	return state


def add_round_key(state, key):

	new = []

	for state_word, key_word in zip(state, key):

		word = []

		for state_byte, key_byte in zip(state_word, key_word):

			word.append(state_byte ^ key_byte)

		new.append(word)
		
	return new

def to_array(text):

	return [int(text[i*2:i*2+2], 16) for i in range(len(text) // 2)]

def to_text(array):

	return ''.join(['{:02x}'.format(i) for i in array])

def mtx_to_text(mtx):

	return ''.join([to_text(array) for array in mtx])

# OFB
def encriptionOFB(block, w, iv):

	last_precipherblock = iv
	remaining_block = [ ]

	encrypted = [ ]

	for word in block:

		for p in word:

			if len(remaining_block) == 0:

				prepd = prepare_key(last_precipherblock)
				b = encryption(prepd, w)
				remaining_block = b[0] + b[1] + b[2] + b[3]
				last_precipherblock = [ ]

			precipherbyte = remaining_block.pop(0)
			last_precipherblock.append(precipherbyte)
			cipherbyte = p ^ precipherbyte
			encrypted.append(cipherbyte)

	return to_text(encrypted)

def decriptionOFB(enc_text, w, iv):

	return encriptionOFB(enc_text, w, iv)


def encriptionECB(block, w):

	i = 0
	l = len(block)
	output = []

	while i < l:

		output += encryption(prepare_key(block[i:i+16]), w)
		i += 16

	return mtx_to_text(output)

def decriptionECB(block, w):

	i = 0
	l = len(block)
	output = []

	while i < l:

		output += decryption(prepare_key(block[i:i+16]), w)
		i += 16

	return mtx_to_text(output)


if __name__=='__main__':

	text = '00112233445566778800112233445566778899aabbccddeeff99aabbccddeeff0011223344556677889900112233445566778899aabbccddeeffaabbccddeeff' 

	key = '000102030405060708090a0b0c0d0e0f1011121314151617'
	iv = 'b7a53ecbbf9d75a0c40efc79b674cc11'
	print('Key: ' + key)
	print('Text: ' + text)

	arr_t = to_array(text)
	arr_k = to_array(key)
	arr_iv = to_array(iv)

	expanded_key = key_expansion(arr_k)
	test = prepare_key(arr_t)

	encryption_ = encryption(test, expanded_key)
	decryption_ = decryption(encryption_, expanded_key)

	print('Encryption result: ' + mtx_to_text(encryption_))
	print('Decryption result: ' + mtx_to_text(decryption_))

	# OFB
	encryptionOFB_ = encriptionOFB(test, expanded_key, arr_iv)
	enc_test = prepare_key(to_array(encryptionOFB_))
	print(enc_test)
	decryptionOFB_ = decriptionOFB(enc_test, expanded_key, arr_iv)

	print('EncryptionOFB result: ' + encryptionOFB_)
	print('DecryptionOFB result: ' + decryptionOFB_)

	# ECB
	encryptionECB_ = encriptionECB(arr_t, expanded_key)
	decryptionECB_ = decriptionECB(to_array(encryptionECB_), expanded_key)

	print('EncryptionECB result: ' + encryptionECB_)
	print('DecryptionECB result: ' + decryptionECB_)
