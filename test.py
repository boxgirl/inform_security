import unittest
from random import randint

from EllipticCurve import EC
from Polynomial import Polynomial

class TestEC(unittest.TestCase):

	def test_random_on_curve(self):
		a = EC.generateRandomPoint()
		self.assertTrue(EC.onCurve(a))

	def test_add_on_curve(self):
		a = EC.generateRandomPoint()
		b = EC.generateRandomPoint()
		c = a + b
		self.assertTrue(EC.onCurve(c))

	def test_add_commutes(self):
		a = EC.generateRandomPoint()
		b = EC.generateRandomPoint()
		self.assertTrue(a + b == b + a)

	def test_double_on_curve(self):
		a = EC.generateRandomPoint()
		b = a + a
		self.assertTrue(EC.onCurve(b))

	def test_mul_on_curve(self):
		a = EC.generateRandomPoint()
		self.assertTrue(EC.onCurve(EC.multiply(a, randint(3, 50))))


unittest.main()
