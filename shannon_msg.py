from gmpy2 import mpz, mpfr
import math
from shannon_p import get_S_ab
import scipy.special

def binomial(n,k):

	if(n < 0): return 0
	if(k < 0): return 0
	if(n < k): return 0
	# C_n^k number of combinations of N things taken k at a time
	return mpz(scipy.special.comb(n, k, exact = 1))


# to be used for message attacks
# probability that a message with e1 +1's and e2 -1's projects onto
# a +1's and b -1's in the last K coordinates
def get_p_msg(N, K, e1, e2, a, b):

	t1 = mpz(binomial(N - K, e1 - a))
	t2 = mpz(binomial(N - K - e1 + a, e2 - b))
	t3 = mpz(binomial(N, e1))
	t4 = mpz(binomial(N - e1, e2))

	return ( mpfr(t1 * t2) / mpfr(t3 * t4) )


# size of the message space M of N-vectors satisfying the dm constraints,
# there are >= dm +1's and >= dm -1's
def get_S_msg(N, dm):

	M = mpz(0)
	for e1 in range(dm, N - dm + 1):
		for e2 in range(dm, N - dm - e1 + 1):
			M += get_S_ab(N, e1, e2)

	return M

# Shannon entropy
# contribution of the (a,b) component to the total entropy
# S(a,b)* p(v_{e1,e2,a,b}) * log_2(p(v_{e1,e2,a,b}))
def get_shannon_p_ab_msg(N, K, e1, e2, a, b):

	p = get_p_msg(N, K, e1, e2, a, b)
	n = get_S_ab(K, a, b)
	u = n * p
	res = mpfr(1)/mpfr(pow(2, 107))
	# discard small contributions that don't matter anyway
	if u < res: return mpfr(0.0)
	return  u * math.log(mpfr(p), 2)


# difficulty of the mitm search for MESSAGE with the hybrid improvement
# p 8-9
def get_shannon_p_msg(N, K, dm, e1, e2):

	# size of message space M satisfying dm constraint
	M = get_S_msg(N, dm)

	# number of elements from T_N(e1, e2) in M
	# T_N - trinary polynomials with e1 +1s and e2 -1s
	m = get_S_ab(N, e1, e2)

	temp = mpfr(0)
	for a in range(0, e1 + 1):
		for b in range(0, e2 + 1):
			temp -= get_shannon_p_ab_msg(N, K, e1, e2, a, b)

	return mpfr(0.5) * mpfr(temp)


# index pairs (i,j) in I(dm) together with the condition i - j = y
# imply that dm <= j = i - y => i >= dm + y
# p 8
def q(e1, e2, y, N, dm):
	# the lowest possible value for i so that i >= dm, and j = (i - y) >= dm
    low = dm + y
    # i < high1 ensures j = (i - y) < N - dm - i <=> 2i < N - dm + y
    h1 = (N - dm + y - 1) // 2 + 1
    # i < high2 is required by definition of I(dm)
    h2 = N - 2*dm
    h = min(h1, h2)
    if low >= h: return mpfr(0)
    t = mpfr(0)
    for i in range(low, h):
        t += binomial(N, i) * binomial(N - i, i - y)

    return -mpfr(math.log(get_S_ab(N, e1, e2), 2 ) - math.log(t))


def get_shannon_p_msg_min(N, K, dm, k):
	# p 9
	# find local minimum, simplification that it will be in extremal points
	e1 = int(round(float(N)/float(3)))
	e2 = e1
	# p 8
	min1 = get_shannon_p_msg(N, K, dm, e1, e2) - q(e1, e2, e1 - e2, N, dm)
	# parameter set secure against hybrid meet-in-the-middle attacks on messages
	if min1 < k:
		return min1
	# |e1-e2| = N - 3*dm
	diff = N - 3*dm
	for e1 in range (dm, N - diff):
		e2 = e1 + diff
		min2 = get_shannon_p_msg(N, K, dm, e1, e2) - q(e1, e2, -diff, N, dm)
		if min2 < min1:
			min1 = min2
			if(min1 < k):
				return min1

	for e1 in range (dm + diff, N):
		e2 = e1 - diff
		min2 = get_shannon_p_msg(N, K, dm, e1, e2) - q(e1, e2, diff, N, dm)
		if min2 < min1:
			min1 = min2
			if(min1 < k):
				return min1

	return min1
