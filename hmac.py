from sha_256 import hashing as hash2
from sha_3 import process as hash3
from binascii import hexlify
# HMAC(k,m) = SHA-3( (k XOR opad)||SHA-256((k XOR ipad)||m) ) 
# opad (outer): 0x5c * n - block, 0x5c - magic number from standard
# ipad (inner): 0x36 * n -block, 0x36 - magic number from standard
# n - block_size in bites
size_h3 = 256

opad = [0x5c]*64
ipad = [0x36]*64
block_size = 64

def hmac(key_, message):

	key_ = list(map(ord, key_))

	if len(key_) > block_size:

		k_i = list(map(ord, hash2(key_)))
		k_o = hash3(key_)

	else:

		k_i = key_ + [0] * (block_size - len(key_))
		k_o= key_ + [0] * (block_size - len(key_))

	ikeypad = [k_i_ ^ ipad_ for k_i_, ipad_ in zip(k_i, ipad)]
	okeypad = [k_o_ ^ opad_ for k_o_, opad_ in zip(k_o, opad)]

	return hash3(bytes(okeypad) + hash2(ikeypad + list(map(ord,message))), size_h3)
	
if __name__=='__main__':

	message = ''
	key = ''
	res = hmac(key, message)
	print('Res: '+ hexlify(res).decode())
