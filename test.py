from sha_256 import *
from sha_3 import *
import unittest
from binascii import hexlify

test_empty = ''
test_abc = 'abc'
test_hard = 'The quick brown fox jumps over the lazy dog'
test_super_hard = 'The quick brown fox jumps over the lazy dog.'
test_sha3_512_empty ='a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a615b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26'
test_sha3_256_abc = '3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532'
test_sha3_hard = '7063465e08a93bce31cd89d2e3ca8f602498696e253592ed26f07bf7e703cf328581e1471a7ba7ab119b1a9ebdf8be41'
test_sha3_super_hard = '1a34d81695b622df178bc74df7124fe12fac0f64ba5250b78b99c1273d4b080168e10652894ecad5f1f4d5b965437fb9'
test_sha256_abc = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
test_sha256_empty = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
test_padding = '61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018'

class TestSHA256(unittest.TestCase):

	def test_sha256_empty(self):
		self.assertEqual(hexlify(hashing(test_empty)).decode(), test_sha256_empty)
	def test_sha256_abc(self):
		self.assertEqual(hexlify(hashing(test_abc)).decode(), test_sha256_abc)
	def test_sha256_padding(self):
		self.assertEqual(hexlify(preprocessing(test_abc)).decode(), test_padding)

class TestSHA3(unittest.TestCase):

	def test_sha3_256(self):
		self.assertEqual(hexlify(process(test_abc, 256)).decode(), test_sha3_256_abc)
	def test_sha3_512(self):
		self.assertEqual(hexlify(process(test_empty,512)).decode(), test_sha3_512_empty)
	def test_sha3_hard(self):
		self.assertEqual(hexlify(process(test_hard,384)).decode(), test_sha3_hard)
	def test_sha3_super_hard(self):
		self.assertNotEqual(hexlify(process(test_sha3_hard,384)).decode(), hexlify(process(test_sha3_super_hard,384)).decode())

unittest.main()
