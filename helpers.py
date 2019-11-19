import math
from sympy.ntheory.generate import nextprime
from gmpy2 import mpz, mpfr
import scipy.special
from shannon_msg import get_shannon_p_msg_min
from shannon_p import get_shannon_p

def get_next_prime(N):

	if(N < 100):
		N = 100

	while(True):
		# infinite list of prime numbers, a dynamically growing sieve of Eratosthenes. 
		# when a lookup is requested involving an odd number that has not been sieved,
		# the sieve is automatically extended up to that number
		N = nextprime(N)
		n = (N - 1)/2
		p = 2
		ok = True
		isTable5 = False # p 17
		if( (mpz(2)**mpz((N - 1)/2) - 1) % N == 0 ):
			isTable5 = True
			p = 3

		if (isTable5):
			if( (mpz(2)**mpz((N - 1)/4) - 1) % N == 0 ):
				continue

			while(n % 2 == 0): n = n // 2

		while(n > 1 and ok):
			if( (mpz(2)**mpz((N - 1)/p) - 1) % N == 0 ):
				ok = False
				break

			while(n % p == 0): n = n // p
			if(n == 1): break
			while(n % p != 0): p = nextprime(p)

		if(ok == True): break

	return N


def binomial(n,k):

	if(n < 0): return 0
	if(k < 0): return 0
	if(n < k): return 0
	# C_n^k number of combinations of N things taken k at a time
	return mpz(scipy.special.comb(n, k, exact = 1))


def dm_valid(N, dm):
	z = mpz(0)
	for i in range(dm, N - 2*dm + 1):
		for j in range(dm, N - dm - i + 1):
			z += binomial(N, i)*binomial(N - i, j)

	if z >= (mpfr(3)**N) * mpfr(1023) / mpfr(1024):
		return True
	else:
		return False

# size of the space of ternary polynomials P_N(d1, d2, d3)
# product form polynomials
# p 10
def get_P_N(N, d1, d2, d3):

	t1 = mpz(binomial(N, d1))
	t2 = mpz(binomial(N - d1, d1))
	t3 = mpz(binomial(N, d2))
	t4 = mpz(binomial(N - d2, d2))
	t5 = mpz(binomial(N, d3))
	t6 = mpz(binomial(N - d3, d3))

	return mpz(t1*t2*t3*t4*t5*t6)

# ( (N-r1)*log_2(q) / (4N^2-4N(K+r1)+(K^2+2*r1*K+r1^2) ) - 1/(2N-(K+r1))
# p 12
def get_eta(N, log2_q, r1, K):
	sec_part = mpfr(2*N - (K + r1))
	eta = mpfr(mpfr((N - r1)*log2_q)/(sec_part*sec_part) - mpfr(1.0)/sec_part)
	return mpz(2)**mpfr(eta)


# experimenal delta* coefficient
def get_delta_star(l):

	if(l <= 60):
		return 1.009
	if(l <= 80):
		return 1.008
	if(l <= 128):
		return 1.007
	if(l <= 256):
		return 1.005
	return 1.0


# cost of hybrid search
# meet-in-the-middle
def get_mitm(N, log2_q, dg, dm, k):

	r1 = k
	for r2 in range(N + 1, 2*N + 1):

		K = 2*N - r2

		# consider only K's for which the cost of lattice reduction is > 2^k (r1 == k)
		eta = get_eta(N, log2_q, r1, K)
		# p 7
		# parameter set resists hybrid meet-in-the-middle attacks on private keys if
		if eta > get_delta_star(k) or eta <= 1:

			continue

		# need to ensure the mitm attack costs at least 2^k (r1 == k)
		k2 = get_shannon_p(N, K, dg)

		if k2 < k:
			# k2 gets smaller as K decreases, so no point to continue
			break

		return k2, K

		# get local_min for message
		k2m = get_shannon_p_msg_min(N, K, dm, k)
		if k2m < k:
			# k2 gets smaller as K decreases, so no point to continue
			break

		return k2, K

	return 0.0, 0
