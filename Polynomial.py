from random import random

class Polynomial:
    def __init__(self, s = None):
        self._poly = s or set()

    def clone(self):
        return Polynomial(self._poly.copy())

    def degree(self):
        max = -1
        for i in self._poly:
            if i > max:
                max = i
        return max

    def tr(self, m, mod):
        t = self.clone()
        for i in range(1, m):
            t = t * t + self
            t = t % mod
        return t

    def htr(self, m, mod):
        t = self.clone()
        for i in range((m - 1) // 2):
            ts = t * t
            t = ts * ts + self
            t = t % mod
        return t

    def __eq__(self, other):
        return self._poly == other._poly

    def __add__(self, q):
        return Polynomial(self._poly ^ q._poly)

    def multHelper(self, i):
        rval = Polynomial()
        for j in self._poly:
            rval._poly.add(i+j)
        return rval

    def __mul__(self, q):
        rval = Polynomial()
        for i in self._poly:
            rval += q.multHelper(i)
        return rval

    def __mod__(self, q):
        return divmod(self, q)[1]

    def __divmod__(self, divisor):
        q = Polynomial()
        d = divisor.degree()
        l = self.clone()
        r = divisor.clone()
        while True:
            shl = l.degree() - d
            if shl < 0:
                return (q, l)
            q += Polynomial({shl})
            l += Polynomial({i + shl for i in r._poly})

    def modExp(self, k, q):
        temp = self.clone()
        rval = Polynomial({0})
        while k > 0:
            if k % 2 == 1:
                rval = (rval * temp) % q
            k //= 2
            temp = (temp * temp) % q
        return rval

    def modMulInv(self, f):
        def egcd(x, y):
            x = (x, Polynomial({0}), Polynomial())
            y = (y, Polynomial(), Polynomial({0}))
            while True:
                q, r = divmod(x[0], y[0])
                if r.degree() < 0:
                    return y
                x, y = y, (r, x[1] + (q * y[1]) % f, x[2] + (q * y[2]) % f)

        g, x, y = egcd(self.clone(), f)
        return x

    def __str__(self):
        if len(self._poly) == 0:
            return "0"
        rval = ""
        a = list(self._poly)
        a = sorted(a, reverse = True)
        return ' + '.join(["z^" + str(i) for i in a])

    def __repr__(self):
        return str(self)

    @staticmethod
    def solve(m, u, w, mod):
        assert(u != Polynomial({0}))
        assert(w != Polynomial({0}))
        wis = w.modMulInv(mod) * w.modMulInv(mod)
        v = u * wis
        if v.tr(m, mod) == Polynomial({1}):
            return None
        return (v.htr(m, mod) * u) % mod

    @staticmethod
    def random(n):
        p = Polynomial()
        for i in range(n+1):
            if(random() > 0.5):
                p._poly.add(i)
        return p
