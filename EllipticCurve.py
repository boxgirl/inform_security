from Polynomial import Polynomial
from collections import namedtuple

Point = namedtuple('Point', 'x y')

class EllipticCurve:
    def __init__(self, a, b, modulus):
        self.a = a
        self.b = b
        self.f = modulus

    def __str__(self):
        s = "y^2 + xy = x^3"
        if self.a != Polynomial():
            s += " + (" + str(self.a) + ")x^2"
        if self.b != Polynomial():
            s += " + (" + str(self.b) + ")"
        return t + s

    def generateRandomPoint(self):
        while True:
            u = Polynomial.random(self.f.degree())
            us = u * u
            w = u * us + self.a * us + self.b
            if u.degree() < 0 or w.degree() < 0:
                continue
            z = Polynomial.solve(self.f.degree(), u, w, self.f)
            if z:
                p = Point(u % self.f, z % self.f)
                print(p)
                if self.onCurve(p):
                    return p

    def onCurve(self, p):
        return (p.y * p.y + p.x * p.x) % self.f == (p.x * p.x + self.a * p.x * p.x + self.b) % self.f

    def add(self, a, b):
        if a == b:
            return self.double(a, b)
        t = (a.y + b.y) + (a.x + b.x).modinv(self.f)
        x = (t * t % self.f + t + a.x + b.x + self.a) % self.f
        return Point(x, t * (a.x + x) % self.f + x + a.y) % self.f

    def double(self, a):
        xis = a.x.modinv(self.f)
        xis = xis * xis % self.f
        x = a.x.modExp(2, self.f) + self.b * xis % self.f
        y = a.x.modExp(2, self.f) + (a.x + a.y * a.x.modinv(self.f) % self.f) * x % self.f + x
        return Point(x, y)
