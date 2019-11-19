from functools import reduce
from math import sqrt

from Polynomial import Polynomial


class Point:
	def __init__(self, x, y, curve):
		self.x = x
		self.y = y
		self._curve = curve

	def clone(self):
		return Point(self.x.clone(), self.y.clone(), self._curve)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __add__(self, other):
		return self._curve.add(self, other)

	def double(self):
		return self._curve.double(self)

	def onCurve(self):
		return self._curve.onCurve(self)

	def isInfinite(self):
		return self.x == Polynomial() and self.y == Polynomial()

class EllipticCurve:
	def __init__(self, a, b, modulus):
		self.a = a
		self.b = b
		self.f = modulus
		self.m = modulus.degree()

	def __str__(self):
		s = "y^2 + xy = x^3"
		if self.a != Polynomial():
			s += " + (" + str(self.a) + ")x^2"
		if self.b != Polynomial():
			s += " + (" + str(self.b) + ")"
		return t + s

	# 6.7 p 11
	def generateRandomPoint(self):
		while True:
			u = Polynomial.random(self.m)
			# z^2+uz=w
			w = u.modExp(3, self.f) + self.a * u * u % self.f + self.b
			if u.degree() < 0 or w.degree() < 0:
				continue
			z = Polynomial.solve(u, w, self.f)
			if z:
				# 6.8 xp=u, yp=z
				return Point(u, z, self)
	# check y^2 + xy = x^3 + B
	def onCurve(self, p):
		return ((p.y * p.y + p.x * p.y) % self.f) == \
			   ((p.x * p.x * p.x + self.a * p.x * p.x + self.b) % self.f)

	def add(self, a, b):
		if a.x != b.x:
			l = (a.y + b.y) * (a.x + b.x).modMulInv(self.f)
			x3 = (l * l % self.f + l + a.x + b.x + self.a) % self.f
			y3 = (l * (a.x + x3) % self.f + x3 + a.y) % self.f
			return Point(x3, y3, self)
		if a.y == b.y:
			return self.double(a)
		return Point(Polynomial(), Polynomial(), self)


	def double(self, p):
		x3 = p.x.modExp(2, self.f) + (self.b * p.x.modMulInv(self.f).modExp(2, self.f)) % self.f
		y3 = p.x.modExp(2, self.f) + ((p.x + (p.y * p.x.modMulInv(self.f)) % self.f) * x3) % self.f + x3
		return Point(x3, y3, self)

	def multiply(self, point, k):
		res = point.clone()
		p = point.clone()
		k -= 1
		while k:
			if k & 1:
				if (res.x == p.x) or (res.y == p.y):
					res = res.double()
				else:
					res = res + p
				k -= 1
			k >>= 1
			p = p.double()
		return res
	'''
	def log(self, p, q):
		if p.isInfinite():
			return -1
		t = 1 << self.m
		n = int(t + 1 + 2 * sqrt(t))
		b = Point(Polynomial(), Polynomial())
		for k in range(1, n + 1):
			b = b + q
			if p == b:
				return k
		return -1
	'''
# y^2 + xy = x^3 + B
EC = EllipticCurve(
		Polynomial(0),
		Polynomial(0x108576C80499DB2FC16EDDF6853BBB278F6B6FB437D9),
		Polynomial(reduce(lambda a, b: a | (1 << b), {173, 10, 2, 1, 0}, 0)))
