import helpers
import random
from primes import get_prime
import hashlib
import fractions
from binascii import hexlify, unhexlify
from sha_256 import hashing


prefixes = b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20'
# key = 1024 bits
# public key
n = 116169470677379136880601217863818349262568478442010864168681707939294733382772665493767578000070487762965366690492174549705615145343554039166153099065910102106103352414659723745586610195947338062846761745176087441561202625599418142717700813833733236525095798695465414527889778229651859962852432925649431830839
e = 65537
# private key
d = 36266067798706661138115272546573561755001293691873617581810937387796215842117236823012004853631416518705310279752271925777835925754252466001188783898240494527599552875783755925959360118167788311317145558202683514441351033892916649670297669916306143983927437267882828496366742107123685066731358528087506793253

message =  b'\xcd\xc8}\xa2#\xd7\x86\xdf;E\xe0\xbb\xbcr\x13&\xd1\xee*\xf8\x06\xcc1Tu\xcco\r\x9cf\xe1\xb6#q\xd4\\\xe29.\x1a\xc9(D\xc3\x10\x10/\x15j\r\x8dR\xc1\xf4\xc4\x0b\xa3\xaae\tW\x86\xcbv\x97W\xa6V;\xa9X\xfe\xd0\xbc\xc9\x84\xe8\xb5\x17\xa3\xd5\xf5\x15\xb2;\x8aA\xe7J\xa8gi?\x90\xdf\xb0a\xa6\xe8m\xfa\xae\xe6Dr\xc0\x0e_ \x94W)\xcb\xeb\xe7\x7f\x06\xcex\xe0\x8f@\x98\xfb\xa4\x1f\x9da\x93\xc01~\x8b`\xd4\xb6\x08J\xcbB\xd2\x9e8\x08\xa3\xbc7-\x85\xe31\x17\x0f\xcb\xf7\xccr\xd0\xb7\x1c)fH\xb3\xa4\xd1\x0fAb\x95\xd0\x80z\xa6%\xca\xb2tO\xd9\xea\x8f\xd2#\xc4%7\x02\x98(\xbd\x16\xbe\x02To\x13\x0f\xd2\xe3;\x93m&v\xe0\x8a\xed\x1bs1\x8bu\n\x01g\xd0'

signature = b'7f50e785a719055cb567e77d75d148fc221e68ed6cfbac4c2e72f09862e7f167f95f5adbc460414d56e6f27a8be3a35f4f384cfb872894b4d42716d010084b2955eaa2042810ff45032da70145a2a3ffe64bb57caee74830f3b52704d8277063e98068b485419dbb55a6a8e8eaafb2a91c68c89ec23695df9819d7368b076858'


class RsaPublicKey(object):

	def __init__(self, n, e):
		self.n = n
		self.e = e
		print('\nRsa public key\nn: {}\ne: {}\nbit_size: {}\n'.format(hex(self.n), self.e, helpers.integer_bit_size(self.n)))

	def rsavp1(self, s):
		if not (0 <= s <= self.n-1):
			raise Exception('\nSignature representative out of range')

		return self.rsaep(s)

	def rsaep(self, m):
		if not (0 <= m <= self.n-1):
			raise Exception('\nMessage representative out of range')
		return pow(m, e, n)

class RsaPrivateKey(object):

	def __init__(self, n, d):
		self.n = n
		self.d = d
		print('\nRsa private key\nn: {}\nd: {}\nbit_size: {}\n'.format(self.n, self.d, helpers.integer_bit_size(self.n)))

	def rsadp(self, c):
		if not (0 <= c <= self.n-1):
			raise Exception('Ciphertext representative out of range')

		return helpers._pow(c, self.d, self.n)

	def rsasp1(self, m):
		if not (0 <= m <= self.n-1):
			raise Exception('Message representative out of range')

		return self.rsadp(m)

# get signature of string using a RSA private key and PKCS#1.5 padding
def sign(private_key, message, prefixes_, hash_class):

	em = encode(message, helpers.integer_byte_size(private_key.n),
			hash_class=hash_class, prefixes__=prefixes_)
	m = helpers.os2ip(em)
	s = private_key.rsasp1(m)
	return helpers.i2osp(s, helpers.integer_byte_size(private_key.n))

# verify a signature of a message using a RSA public key and PKCS#1.5 padding
def verify(public_key, message_, signature_, prefixes_, hash_class):

	if len(signature_) != helpers.integer_byte_size(public_key.n):
		raise Exception('Invalid signature')
	s = helpers.os2ip(signature_)
	try:
		m = public_key.rsavp1(s)
	except ValueError:
		raise Exception('Invalid signature')
	try:
		em = helpers.i2osp(m, helpers.integer_byte_size(public_key.n))
	except ValueError:
		raise Exception('Invalid signature')
	try:
		em_prime = encode(message_, helpers.integer_byte_size(public_key.n),
				hash_class=hash_class,  prefixes__=prefixes_)
	except ValueError:
		raise Exception('RSA mod (n) too short')

	return helpers.constant_time_cmp(em, em_prime)


def encode(message, em_len, prefixes__, hash_class, ps=None):
	if hash_class == hashlib.sha1:

		halgo = hash_class(message)
		h = halgo.digest()
	else:
		h = hashing(hexlify(message).decode())

	t = prefixes__ + h
	
	if em_len < len(t) + 11:
		raise Exception('Message too short')
	ps_len = em_len - len(t) - 3
	ps = b'\xff' * ps_len
	return b'\x00\x01' + ps + b'\x00' + t



def generate_key_pair(size=1024, number=2, k=1000, strict_size=True, e=0x10001):

	# size: the bit size of the mod
	# number: the number of primes 
	# strict_size: whether to use size as a lower bound or a strict goal
	rnd=random.SystemRandom()
	primes = []
	lbda = 1
	bits = size // number + 1
	n = 1
	while len(primes) < number:
		if number - len(primes) == 1:
			bits = size - helpers.integer_bit_size(n) + 1
		prime = get_prime(bits, k)
		if prime in primes:
			continue
		if e is not None and fractions.gcd(e, lbda) != 1:
			continue
		if strict_size and number - len(primes) == 1 and helpers.integer_bit_size(n*prime) != size:
			continue
		primes.append(prime)
		n *= prime
		lbda *= prime - 1
	print([hex(prime) for prime in primes])

	if e is None:
		e = 0x10001
		while e < lbda:
			if fractions.gcd(e, lbda) == 1:
				break
			e += 2
	assert 3 <= e <= n-1
	public = RsaPublicKey(n, e)
	private = RsaPrivateKey(n, d)
	return public, private

#MAIN

def test_rsassa_pkcs1_v15_sign(signature, message, private_key):

	assert len(signature) == helpers.integer_byte_size(private_key.n)
	print('My signature')
	print(hexlify(sign(private_key, message)).decode())
	print('Real signature')
	print(hexlify(signature).decode())
	assert sign(private_key, message) == signature


def test_rsassa_pkcs1_v15_verify(signature, message, public_key):

	assert len(signature) == helpers.integer_byte_size(public_key.n)
	assert verify(public_key, message, signature)

if __name__ == '__main__':

	#public_key, private_key = generate_key_pair(e=e)
	public_key = RsaPublicKey(n=n,e=e)
	private_key = RsaPrivateKey(n=n,d=d)
	signature = unhexlify(signature)
	test_rsassa_pkcs1_v15_sign(signature, message, private_key)

	test_rsassa_pkcs1_v15_verify(signature, message, public_key)
