from random import getrandbits

class Polynomial:
	def __init__(self, p=0):
		self._poly = p

	def clone(self):
		return Polynomial(self._poly)

	def degree(self):
		return self._poly.bit_length() - 1

	# 6.5 p 11
	def tr(self, mod):
		t = self.clone()
		for i in range(1, mod.degree()):
			t = t.modExp(2, mod) + self
		return t
	# 6.6 p 11
	def htr(self, mod):
		t = self.clone()
		for i in range((mod.degree() - 1) // 2):
			t = t.modExp(4, mod) + self
		return t

	def __eq__(self, other):
		return self._poly == other._poly

	def __add__(self, q):
		return Polynomial(self._poly ^ q._poly)

	def __mul__(self, q):
		p = self._poly
		q = q._poly
		if not q:
			return Polynomial()
		rval = 0
		while p:
			if p & 1:
				rval ^= q
			p >>= 1
			q <<= 1
		return Polynomial(rval)

	def __divmod__(self, divisor):
		q = 0
		bl = divisor.degree() + 1
		this = self._poly
		divisor = divisor._poly
		while True:
			shift = this.bit_length() - bl
			if shift < 0:
				return (Polynomial(q), Polynomial(this))
			q ^= 1 << shift
			this ^= divisor << shift

	def __mod__(self, other):
		return divmod(self, other)[1]

	def modExp(self, k, q):
		temp = self.clone()
		rval = Polynomial(1)
		while k > 0:
			if k % 2 == 1:
				rval = (rval * temp) % q
			k //= 2
			temp = (temp * temp) % q
		return rval

	def modMulInv(self, m):
		def egcd(x, y):
			x = (x, Polynomial(1), Polynomial())
			y = (y, Polynomial(), Polynomial(1))
			while True:
				q, r = divmod(x[0], y[0])
				if r.degree() < 0:
					return y
				x, y = y, (r, x[1] + (q * y[1]), x[2] + (q * y[2]))
		g, x, y = egcd(self.clone(), m)
		if g._poly != 1:
			raise Exception('modular inverse does not exist')
		else:
			return x

	def __str__(self):
		if self._poly == 0:
			return "0"
		a = [i[0] for i in enumerate(reversed(bin(self._poly)[2:])) if i[1] == '1']
		return ' + '.join("x^" + str(i) for i in reversed(a))

	def __repr__(self):
		return str(self)

	@staticmethod
	def random(n):
		return Polynomial(getrandbits(n))

	@staticmethod
	def solve(u, w, mod):
		# v= wu^-2
		ui = u.modMulInv(mod)
		v = w * ui * ui % mod
		if v.tr(mod) == Polynomial(1):
			return None
		return (v.htr(mod) * u) % mod

