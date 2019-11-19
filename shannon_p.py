from gmpy2 import mpz, mpfr
import math
import scipy.special

def binomial(n,k):

	if(n < 0): return 0
	if(k < 0): return 0
	if(n < k): return 0
	# C_n^k number of combinations of N things taken k at a time
	return mpz(scipy.special.comb(n, k, exact = 1))


# p(v_{a,b}) = ( (N-K  d-a ) (N-K-d+a   d+1-b) )/ ( (N d) (N-d d+1))
# for a polynomial with d 1's and (d+1) -1's, what is the probability
# that the last K coordiantes contain a +1's and b -1's
# p 6
def get_p(N, K, d, a, b):
	t1 = mpz(binomial(N - K, d - a))
	t2 = mpz(binomial(N - K - d + a, d + 1 - b))
	t3 = mpz(binomial(N, d))	
	t4 = mpz(binomial(N - d, d + 1))

	return ( mpfr(t1 * t2) / mpfr(t3 * t4) )

# ( K a) ( K-a b)
# number of choices of distinct v_{a,b}
# how many was are there of selecting a +1's and b -1's from K coordinates
def get_S_ab(K, a, b):

	t1 = mpz(binomial(K, a))
	t2 = mpz(binomial(K - a, b))

	return ( mpz(t1 * t2) )


# Shannon entropy
# S(a,b)* p(v_{a,b}) * log_2(p(v_{a,b}))
# contribution to the total entropy from the (a,b) component
def shannon_p_ab(N, K, d, a, b):

	p = get_p(N, K, d, a, b)
	n = get_S_ab(K, a, b)
	u = n * p
	res = mpfr(1)/mpfr(pow(2, 107))
	# discard small contributions that don't matter anyway
	if u < res: return mpfr(0.0)
	return u * math.log(mpfr(p), 2)



# difficulty of the mitm search for KEY with the hybrid improvement
# Snannon entropy of p
# H(p) = -sum( S(a,b)* p(v_{a,b}) * log_2(p(v_{a,b})) )
# p 6-7
def get_shannon_p(N, K, d):

	temp = mpfr(0)

	for a in range(0, d + 1):
		for b in range(0,  d + 2):
			temp -= shannon_p_ab(N, K, d, a, b)
	# 1/2 * H(p) - log_2(N)
	res = ( mpfr(0.5)*mpfr(temp - math.log(N, 2)) )

	return res
