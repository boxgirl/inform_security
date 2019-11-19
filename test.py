import unittest
from helpers import binomial, get_P_N, get_mitm, get_next_prime
from shannon_p import get_shannon_p
from main import create_keys, param_gen, encrypt, decipher, gen_random_string

class TestHelpers(unittest.TestCase):

	def test_binomial(self):
		self.assertEqual(binomial(4,2), 6)
		self.assertEqual(binomial(123,65), 626530645220345271243285139240656129)
		self.assertEqual(binomial(23,15), 490314)
		self.assertEqual(binomial(233,155), 1786364572172824703996858613353160486834994843862378906323850064)

	def test_get_next_prime(self):
		self.assertEqual(get_next_prime(100), 101)
		self.assertEqual(get_next_prime(101), 103)
		self.assertEqual(get_next_prime(1427), 1439)
	
	def test_get_P_N(self):
		self.assertEqual(get_P_N( 20 , 3 , 3 , 3 ), 465844843008000000 )
		self.assertEqual(get_P_N( 20 , 3 , 3 , 4 ), 5298985089216000000 )
		self.assertEqual(get_P_N( 20 , 3 , 4 , 3 ), 5298985089216000000 )
		self.assertEqual(get_P_N( 349 , 5 , 4 , 3 ), 27691700021979688642069166913786224212351789693996800 )
		self.assertEqual(get_P_N( 349 , 5 , 5 , 4 ), 941549482821304560792127066402597686039082201278480101738880 )

	def test_get_shannon_p(self):

		self.assertAlmostEqual(get_shannon_p(401, 131, 113),  97.377083840317757911093337789895373407334)
		self.assertAlmostEqual(get_shannon_p(401, 154, 133), 117.64544671566375467936245484379700328014)
		self.assertAlmostEqual(get_shannon_p(439, 174, 146), 133.42409866220694)

	def test_mitm(self):
		self.assertAlmostEqual(get_mitm(541, 11, 180, 144, 128)[0], 255.94886636663188)


params = (401, 2048, 8, 8, 6, 134, 102, 3)
len_b = 10
m0 = 'hello!'
m1 = '123 hello world...'
m2 = '9a1549r828213045k079212706640kl2275k'
m3 = 'the brown crazy fox jumps under lazy dog.'

class TestProcess(unittest.TestCase):

	def test_create_keys(self):
		#params = param_gen(128)
		_,_,_,g = create_keys(params)

		self.assertEqual(g.coefficients().count(1), 135)
		self.assertEqual(g.coefficients().count(-1), 134)

	def test_enc_dec(self):
		
		public_key, private_key, R, _ = create_keys(params)
		for m in [m0, m1, m2, m3]:
			secret = encrypt(m, public_key, R, len_b, params)
			msg = decipher(secret, R, private_key[0], params, public_key, len_b)
			self.assertEqual(msg, m)


unittest.main()
