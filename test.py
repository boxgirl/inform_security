from Polynomial import Polynomial
from EllipticCurve import EllipticCurve

p = Polynomial({173, 10, 2, 1, 0})

B = 0x108576C80499DB2FC16EDDF6853BBB278F6B6FB437D9
q = Polynomial()
q._poly = set([idx for idx, i in enumerate(list(reversed("{0:b}".format(B)))) if i == '1'])

print(p)
print(q)

c = EllipticCurve(Polynomial(), q, p)
print(c.onCurve(c.generateRandomPoint()))
