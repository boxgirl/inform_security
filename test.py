from rsa_dsa import *
import unittest
from binascii import hexlify, unhexlify
import helpers
import hashlib
import sha_256
test_e = 65537
test_message =  b'\xcd\xc8}\xa2#\xd7\x86\xdf;E\xe0\xbb\xbcr\x13&\xd1\xee*\xf8\x06\xcc1Tu\xcco\r\x9cf\xe1\xb6#q\xd4\\\xe29.\x1a\xc9(D\xc3\x10\x10/\x15j\r\x8dR\xc1\xf4\xc4\x0b\xa3\xaae\tW\x86\xcbv\x97W\xa6V;\xa9X\xfe\xd0\xbc\xc9\x84\xe8\xb5\x17\xa3\xd5\xf5\x15\xb2;\x8aA\xe7J\xa8gi?\x90\xdf\xb0a\xa6\xe8m\xfa\xae\xe6Dr\xc0\x0e_ \x94W)\xcb\xeb\xe7\x7f\x06\xcex\xe0\x8f@\x98\xfb\xa4\x1f\x9da\x93\xc01~\x8b`\xd4\xb6\x08J\xcbB\xd2\x9e8\x08\xa3\xbc7-\x85\xe31\x17\x0f\xcb\xf7\xccr\xd0\xb7\x1c)fH\xb3\xa4\xd1\x0fAb\x95\xd0\x80z\xa6%\xca\xb2tO\xd9\xea\x8f\xd2#\xc4%7\x02\x98(\xbd\x16\xbe\x02To\x13\x0f\xd2\xe3;\x93m&v\xe0\x8a\xed\x1bs1\x8bu\n\x01g\xd0'
signature = unhexlify(b'7f50e785a719055cb567e77d75d148fc221e68ed6cfbac4c2e72f09862e7f167f95f5adbc460414d56e6f27a8be3a35f4f384cfb872894b4d42716d010084b2955eaa2042810ff45032da70145a2a3ffe64bb57caee74830f3b52704d8277063e98068b485419dbb55a6a8e8eaafb2a91c68c89ec23695df9819d7368b076858')

prefixes_sha1 =  b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14'
prefixes = b'\x30\x31\x30\x0d\x06\x09\x60\x86\x48\x01\x65\x03\x04\x02\x01\x05\x00\x04\x20'

n = 116169470677379136880601217863818349262568478442010864168681707939294733382772665493767578000070487762965366690492174549705615145343554039166153099065910102106103352414659723745586610195947338062846761745176087441561202625599418142717700813833733236525095798695465414527889778229651859962852432925649431830839
e = int('010001', 16)
d = 36266067798706661138115272546573561755001293691873617581810937387796215842117236823012004853631416518705310279752271925777835925754252466001188783898240494527599552875783755925959360118167788311317145558202683514441351033892916649670297669916306143983927437267882828496366742107123685066731358528087506793253

test_message2 = unhexlify('cdc87da223d786df3b45e0bbbc721326d1ee2af806cc315475cc6f0d9c66e1b62371d45ce2392e1ac92844c310102f156a0d8d52c1f4c40ba3aa65095786cb769757a6563ba958fed0bcc984e8b517a3d5f515b23b8a41e74aa867693f90dfb061a6e86dfaaee64472c00e5f20945729cbebe77f06ce78e08f4098fba41f9d6193c0317e8b60d4b6084acb42d29e3808a3bc372d85e331170fcbf7cc72d0b71c296648b3a4d10f416295d0807aa625cab2744fd9ea8fd223c42537029828bd16be02546f130fd2e33b936d2676e08aed1b73318b750a0167d0')
test_signature = unhexlify('6bc3a06656842930a247e30d5864b4d819236ba7c68965862ad7dbc4e24af28e86bb531f03358be5fb74777c6086f850caef893f0d6fcc2d0c91ec013693b4ea00b80cd49aac4ecb5f8911afe539ada4a8f3823d1d13e472d1490547c659c7617f3d24087ddb6f2b72096167fc097cab18e9a458fcb634cdce8ee35894c484d7')

class TestRSAVerify(unittest.TestCase):

	def test_len_public(self):
		public_key, private_key = generate_key_pair(e=test_e)
		self.assertEqual(len(signature), helpers.integer_byte_size(public_key.n))
	def test_value_verify(self):
		public_key = RsaPublicKey(n=n,e=e)
		self.assertEqual(verify(public_key, test_message, signature, hash_class=sha_256, prefixes_=prefixes), True)
	def test_value_verify2(self):
		public_key = RsaPublicKey(n=n,e=e)
		self.assertEqual(verify(public_key, test_message2, test_signature, hash_class=hashlib.sha1, prefixes_=prefixes_sha1), True)

class TestRSASign(unittest.TestCase):

	def test_len_private(self):
		public_key, private_key = generate_key_pair(e=test_e)
		self.assertEqual(len(signature), helpers.integer_byte_size(private_key.n))
	def test_sign(self):
		private_key = RsaPrivateKey(n=n,d=d)
		self.assertEqual(sign(private_key, test_message, hash_class=hashlib.sha256, prefixes_=prefixes), signature)

	def test_sign2(self):
		private_key = RsaPrivateKey(n=n,d=d)
		self.assertEqual(sign(private_key, test_message2, hash_class=hashlib.sha1, prefixes_=prefixes_sha1), test_signature)
unittest.main()
