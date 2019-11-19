import fractions
import helpers
import random

num_iter = 1000

# test if n is a prime number
def is_prime(n, k=num_iter):

	# miller rabin probability of primality is 1/4**k
	return miller_rabin(n, k)


def get_prime(size=256, k=num_iter):

	rnd=random.Random()
	while True:

		n = rnd.getrandbits(size-2)
		n = 2 ** (size-1) + n * 2 + 1

		if is_prime(n, k=k):
			return n


def miller_rabin(n, k):

	# n - the integer number to test,
	# k - the number of iteration, the probability of n being prime if the algorithm returns True is 1/2**k,
	rnd=random.Random()
	s = 0
	d = n-1
	# Find nearest power of 2
	s = helpers.integer_bit_size(n)
	# Find greatest factor which is a power of 2
	s = fractions.gcd(2**s, n-1)
	d = (n-1) // s
	s = helpers.integer_bit_size(s) - 1
	while k:
		k = k - 1
		a = rnd.randint(2, n-2)
		x = pow(a,d,n)
		if x == 1 or x == n - 1:
			continue
		for r in range(1,s-1):
			x = pow(x,2,n)
			if x == 1:
				return False
			if x == n - 1:
				break
		else:
			return False
	return True
