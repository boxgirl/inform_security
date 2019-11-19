import os
from binascii import hexlify, unhexlify
from hmac import hmac
from EllipticCurve import EC
from aes_192 import  *
from rsa_dsa import *
import hashlib
import sha_256
import helpers


prefixes = b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20'
n = 116169470677379136880601217863818349262568478442010864168681707939294733382772665493767578000070487762965366690492174549705615145343554039166153099065910102106103352414659723745586610195947338062846761745176087441561202625599418142717700813833733236525095798695465414527889778229651859962852432925649431830839
d = 36266067798706661138115272546573561755001293691873617581810937387796215842117236823012004853631416518705310279752271925777835925754252466001188783898240494527599552875783755925959360118167788311317145558202683514441351033892916649670297669916306143983927437267882828496366742107123685066731358528087506793253
e = int('010001', 16)
signature = unhexlify(b'7f50e785a719055cb567e77d75d148fc221e68ed6cfbac4c2e72f09862e7f167f95f5adbc460414d56e6f27a8be3a35f4f384cfb872894b4d42716d010084b2955eaa2042810ff45032da70145a2a3ffe64bb57caee74830f3b52704d8277063e98068b485419dbb55a6a8e8eaafb2a91c68c89ec23695df9819d7368b076858')
# p, g - not secret values
a = 'Alice'
b = 'Bob'


def sign_point(g):
	x_str = padding_pol(g.x)
	y_str = padding_pol(g.y)
	to_sign = x_str + y_str
	private_key = RsaPrivateKey(n=n,d=d)
	return to_sign, sign(private_key, unhexlify(to_sign), hash_class=hashlib.sha256, prefixes_=prefixes)


def sign_points(g1, g2):
	to_sign = pad_point(g1) + pad_point(g2)
	private_key = RsaPrivateKey(n=n,d=d)
	to_sign = to_sign.encode()
	return to_sign, sign(private_key, to_sign, hash_class=hashlib.sha256, prefixes_=prefixes)


def encryption(message, k):
	lenm = len(message)
	if lenm % 16 != 0:
		message = message + b' ' * (16 - lenm%16)
	arr_t = to_array(hexlify(message))
	arr_k = to_array(hexlify(k))
	expanded_key = key_expansion(arr_k)
	encryptionECB_ = encriptionECB(arr_t, expanded_key)
	return expanded_key, encryptionECB_


def decryption(ciphertext, expanded_key):

	decryptionECB_ = decriptionECB(to_array(ciphertext), expanded_key)
	return decryptionECB_

def gen_secret_key(numBits=24):

	return int.from_bytes(os.urandom(numBits // 8), byteorder='big')


def gen_public_key(g, k):

	return EC.multiply(g, k)


def padding_pol(p):

	p_str = '{0:b}'.format(p._poly)
	p_str = '0' * (173 - len(p_str)) + p_str
	return p_str


def pad_point(p):
	x_str = padding_pol(p.x)
	y_str = padding_pol(p.y)
	return x_str + y_str


def get_param():

	g = EC.generateRandomPoint()
	a_sc = gen_secret_key(24)
	b_sc = gen_secret_key(24)

	print('secret keys: %d, %d' % (a_sc, b_sc))
	# A -> B: g^x
	gx = gen_public_key(g, a_sc)

	# B -> A: g^y, B, SIG_B(g^x, g^y), MAC_km(B)
	b_common_k = EC.multiply(gx, b_sc)
	print('Bob\'s common_key (secret): {}'.format(b_common_k))
	gy = gen_public_key(g, b_sc)
	to_sign_b, signed_b = sign_points(gx, gy)

	# A -> B: A, SIG_A(g^y, g^x), MAC_km(A)
	a_common_k = EC.multiply(gy, a_sc)
	print('Alice\'s common_key (secret): {}'.format(a_common_k))
	to_sign_a, signed_a = sign_points(gy, gx)
	return g, a_sc, b_sc, gx, gy, b_common_k, a_common_k, signed_a, signed_b, to_sign_a, to_sign_b

# SIGMA: Basic Version
def sigma():
	g, a_sc, b_sc, gx, gy, b_common_k, a_common_k, signed_a, signed_b,_,_ = get_param()

	km = str(gen_secret_key(24))

	mac_b = hmac(km, b)
	public_key, private_key = generate_key_pair(e=e)
	print(b_common_k == a_common_k)
	check_bob_key = verify(public_key, signed_b, signature, hash_class=sha_256, prefixes_=prefixes)
	check_bob_id = hmac(km, b) == mac_b
	mac_a = hmac(km, a)

	# check signed by Alice key
	check_alice_key = verify(public_key, signed_a, signature, hash_class=sha_256, prefixes_=prefixes)
	check_alice_id = hmac(km, a) == mac_a

	print('Bob\'s key verification: {}'.format(check_bob_key))
	print('Alice\'s key verification: {}'.format(check_alice_key))
	print('Bob\'s id verification: {}'.format(check_bob_id))
	print('Alice\'s id verification: {}'.format(check_alice_id))

# SIGMA-I: active protection of Initiators id
def sigma_i():

	g, a_sc, b_sc, gx, gy, b_common_k, a_common_k, signed_a, signed_b, to_sign_a, to_sign_b = get_param()

	km = str(gen_secret_key())
	ke = os.urandom(24)

	mac_b = hmac(km, b)
	#sign_t = signed_b['signature'].hex()
	to_encr = b.encode() + b' ' + to_sign_b + b' ' + signed_b + b' ' + bytes(mac_b)
	expanded_key, encr_b = encryption(to_encr, ke)
	public_key, private_key = generate_key_pair(e=e)

	signed_b_sign_retr,  = decryption(encr_b, expanded_key).split(' ')[:4]
	mac_b_retr = hmac(str(ke), encr_b)

	check_bob_key = verify(public_key, signed_b_sign_retr.encode(), signature, hash_class=sha_256, prefixes_=prefixes)

	check_bob_id = hmac(km, b) == mac_b_retr

	mac_a = hmac(km, a)

	to_encr = a.encode() + b' ' + to_sign_a + b' ' + signed_a + b' ' + bytes(mac_a)
	expanded_key, encr_a = encryption(to_encr, ke)

	signed_a_sign_retr,  = decryption(encr_a, expanded_key).split(' ')[:4]
	mac_a_retr = hmac(str(ke), encr_a)
		
	check_alice_key = verify(public_key, signed_a_sign_retr.encode(), signature, hash_class=sha_256, prefixes_=prefixes)
	check_alice_id = hmac(km, a) == mac_a_retr


	print(b_common_k == a_common_k)

	print('Bob\'s key verification: {}'.format(check_bob_key))
	print('Alice\'s key verification: {}'.format(check_alice_key))
	print('Bob\'s id verification: {}'.format(check_bob_id))
	print('Alice\'s id verification: {}'.format(check_alice_id))


# SIGMA-R : active protection of Responders id
def sigma_r():
	g, a_sc, b_sc, gx, gy, b_common_k, a_common_k, signed_a, signed_b, to_sign_a, to_sign_b = get_param()

	km1 = str(gen_secret_key())
	km2 = str(gen_secret_key())
	ke1 = os.urandom(24)
	ke2 = os.urandom(24)
	public_key, private_key = generate_key_pair(e=e)
	mac_a = hmac(km1, a)
	to_encr = a.encode() + b' ' + to_sign_a + b' ' + signed_a + b' ' + bytes(mac_a)
	expanded_key, encr_a = encryption(to_encr, ke1)

	# B -> A: {B, SIG_B(g^x, g^y), MAC_km(A)}_ke
	signed_a_sign_retr,  = decryption(encr_a, expanded_key).split(' ')[:4]
	mac_a_retr = hmac(str(ke1), encr_a)
	
	check_alice_key = verify(public_key, signed_a_sign_retr.encode(), signature, hash_class=sha_256, prefixes_=prefixes)
	check_alice_id = hmac(km1, a) == mac_a_retr

	mac_b = hmac(km2, b)

	to_encr = b.encode() + b' ' + to_sign_b + b' ' + signed_b + b' ' + bytes(mac_b)
	expanded_key, encr_b = encryption(to_encr, ke2)

	# check signed by Alice key
	signed_b_sign_retr = unhexlify(decryption(encr_b, expanded_key)).split(b' ')[:4]
	mac_b_retr = hmac(str(ke2), encr_b)
	check_bob_key = verify(public_key, signed_b_sign_retr[2], signature, hash_class=sha_256, prefixes_=prefixes)
	check_bob_id = hmac(km2, b) == mac_b_retr
	
	print(b_common_k == a_common_k)

	print('Bob\'s key verification: {}'.format(check_bob_key))
	print('Alice\'s key verification: {}'.format(check_alice_key))
	print('Bob\'s id verification: {}'.format(check_bob_id))
	print('Alice\'s id verification: {}'.format(check_alice_id))


if __name__=='__main__':
	sigma()
	print('______________________________________________________________________')
	sigma_i()
	print('______________________________________________________________________')
	sigma_r()
