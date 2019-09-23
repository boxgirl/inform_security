from aes_192 import *
import unittest


def conv(x):
    return prepare_key(to_array(x))

test_input = conv('00112233445566778899aabbccddeeff')

test_key0 = conv('000102030405060708090a0b0c0d0e0f')
test_input_d = conv('793e76979c3403e9aab7b2d10fa96ccc')
test_inv_row = conv('79a9b2e99c3e6cd1aa3476cc0fb70397')
test_inv_sub_bytes = conv('afb73eeb1cd1b85162280f27fb20d585')
test_inv_mcol = conv('c494bffae62322ab4bb5dc4e6fce69dd')
test_inv_state = conv('71d720933b6d677dc00b8f28238e0fb7')
test_start = conv('00102030405060708090a0b0c0d0e0f0')
test_sbox = conv('63cab7040953d051cd60e0e7ba70e18c')
test_srow = conv('6353e08c0960e104cd70b751bacad0e7')
test_mcol = conv('5f72641557f5bc92f7be3b291db9f91a')

test_sbox_ = conv('63cab7040953d051cd60e0e7ba70e18c')
test_srow_ = conv('6353e08c0960e104cd70b751bacad0e7')

class TestEncryptMethods(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add_round_key(test_input, test_key0), test_start)
    def test_sbox(self):
        self.assertEqual(sub_bytes(test_start), test_sbox)
    def test_srow(self):
    	self.assertEqual(shift_rows(test_sbox_), test_srow_)
    def test_mcol(self):
    	self.assertEqual(mix_columns(test_srow), test_mcol)

class TestDecryptMethods(unittest.TestCase):
   
    def test_inv_sbox(self):
        self.assertEqual(inv_sub_bytes(test_inv_row), test_inv_sub_bytes)
    def test_inv_srow(self):
    	self.assertEqual(inv_shift_rows(test_input_d), test_inv_row)
    def test_inv_mcol(self):
    	self.assertEqual(inv_mix_columns(test_inv_state), test_inv_mcol)

unittest.main()
