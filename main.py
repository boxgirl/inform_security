
import numpy as np
import math
from gmpy2 import mpz, mpfr
import scipy.special
from collections import Counter
from sage.all import *
from helpers import *
import random
from sha_256 import hashing
import string

# k - k-bit security
# p - message space modulus (param in poly), (-p/2, p/2]
# N, q - ring param: N - size of poly and prime;  (-q/2, q/2] 
# p and q can be not primes, but  gcd=1
# d1-3 -  non-zero coefficient counts for product form polynomial terms
# dg - non-zero coefficient count for private key component g
# dm - message representative Hamming weight constraint


def param_gen(k):

	# init value
	N = 0
	d1 = 0
	d2 = 0
	d3 = 0
	dg = 0
	dm = 0
	q = 0
	k1 = 0
	k2 = 0
	pdf = 0
	K = 0

	while(True):
		print('Iteration')
		# find params N, d1, d2, d3, dg, dm
		while(True):

			N = get_next_prime(N)

			# [N/3]
			dg = int(math.floor(float(N)/float(3) + 0.5))

			# [1/4* sqrt(1+8*N/3)-1]
			d1 = int(math.ceil(0.25*(math.sqrt(1 + float(8*N)/float(3)) - 1)))

			# [(N//3-d1)/(2*d1)]
			d2 = int(math.ceil((float(N)/float(3) - d1)/float(2*d1)))

			# max([d3/2+1], [N/3-2*d1*d2])
			d3 = int(max(math.ceil(float(d1)*0.5 + 1), math.ceil(float(N)/float(3) - 2*d1*d2)))

			# the largest value satisfying 
			
			r1 = 0
			r2 = N
			while(r1 < r2 - 1):
				r3 = (r1 + r2) // 2
				if(dm_valid(N, r3)):
					r1 = r3
				else:
					r2 = r3
			dm = r1

			# [1/2*log_2(|P_N(d1, d2, d3)|/N)]
			# cost of direct combinatorial search gives an upper bound on the security
			k1 = mpz(0.5*math.log(mpfr(get_P_N(N, d1, d2, d3))/mpfr(N), mpfr(2)))

			# cost of combinatorial search is k1
			if(k1 >= k):
				break


		# ( (4*d1*d2+2*d3) * ((N-dm+2*dg+1)/N) )^1/2
		sigma = math.sqrt( (4*d1*d2 + 2*d3) * (float(N - dm + 2*dg + 1)/float(N)) )

		# this step makes sure the risk of decryption failure is < 2^{-k}
		# by making q large enough - q not used so far
		# the smallest power of 2 satisfying
		q = mpz(2)
		log2_q = 1
		two_pow_k1 = mpfr(pow(2, k1))

		while(True):
			# probability of decription fail 
			# N * (erfc( (q-2)/(6*sqrt(2*sigma)) ) )
			# erfc term - p = 3 is implicit (factor 6 in denominator is 3p)
			# erfc(x) = 1.0 - erf(x), complementary error function at x
			# erf(x) for a random variable Y that is normally distributed with 
			# mean 0 and variance 1/2, describes the probability of Y falling in the range [−x, x]. 
			pdf = mpfr(N * math.erfc((q - 2)/(6*math.sqrt(2)*sigma)))
			if (pdf * two_pow_k1) < 1:
				break
			q = mpz(2*q)
			log2_q += 1

		# meet-in-the-middle
		# k2 - cost of hybrid search
		# K - hybrid parameter that minimizes the maximum of the cost estimates for hybrid attacks
		k2, K = get_mitm(N, log2_q, dg, dm, k)

		flag = True
		while(flag):
			# the parameter is not strong enough for the mitm attack
			if k2 < k:
				break

			# check ability to use half of q, because (-q/2, q/2)
			q_half = q // 2

			# prob for half of decryption fail
			# N * (erfc( (q//2-2)/(6*sqrt(2*sigma)) ) )
			pdfh = mpfr(N * math.erfc((q_half - 2)/(6*math.sqrt(2)*sigma)))
			if pdfh * mpfr(pow(2, k)) < 1:

				q = q_half
				log2_q -= 1
				k2h, Kh = get_mitm(N, log2_q, dg, dm, k)
				# the parameter is strong enough for the mitm attack
				if k2h >= k:

					if k2h > k2:
						k2 = k2h
						K = Kh
						pdf = pdfh

					flag = False
			else:
				# just keep the original q
				flag = False

		# if flag == True, k2 was too small
		if(not flag):
			break
	print('Decryption fail prob: ', pdf)
	print('K: {}\ncost of direct combinatorial search: {}\ncost of hybrid search: {}'. format(K, k1, k2))

	return N, int(q), d1, d2, d3, dg, dm


def generate_random(lower, upper, R_, N):

	lower_array = [-1] * lower
	upper_array = [1] * upper
	zero_array = [0] * (N - (lower + upper))
	poly = lower_array + upper_array + zero_array
	random.shuffle(poly)

	return R_(poly)


def mod(poly, num, R_):

	coefs = poly.list()

	for i in range(len(coefs)):
		coefs[i] = Mod(coefs[i], num)
	return R_(coefs)


def recenter(poly, num, R_):

	coefs = poly.list()
	limit = num//2

	for i in range(len(coefs)):
		coefs[i] = Mod(coefs[i], num)
		if coefs[i] > limit:
			coefs[i] = int(coefs[i]) - num
	return R_(coefs)

# p 2
def create_keys(params):
	N, q, d1, d2, d3, dg, dm, p = params
	R = PolynomialRing(QQ, 'x')
	x = R.gen()
	gcd = 0

	while gcd != 1:
		# poly with df1 +1s and df2 -1s, else coeff=0
		f1 = generate_random(d1, d1, R, N)
		f2 = generate_random(d2, d2, R, N)
		f3 = generate_random(d3, d3, R, N)
		# Lf: f = 1+pF
		f = 1 + ((p)* (((f1 * f2) % (x**N - 1)) + f3))
		# Lg: g poly
		g = generate_random(dg, dg + 1, R, N)
		extended_gcd = xgcd(x**N -1, f)
		gcd = extended_gcd[0]
		v = extended_gcd[2]
	# fp(x)*f(x)=1 mod p и fq(x)*f(x)=1 mod q
	fp = mod(v, p, R)
	fq = mod(v, q, R)
	# public key: h = f^(-1)*g
	# h(x)=fq(x)*g(x) mod q
	h = recenter((p * fq * g) % (x**N - 1), q, R)
	#print("fq: {}".format(fq))
	#print("g: {}".format(g))
	#print("fp: {}".format(fp))
	#print("f: {}".format(f))
	#print("h: {}".format(h))
	# public and private (f(x),fp(x))
	return h, (f, fp), R, g


def gen_random_string(size):

	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def encode(message):

	bit_list = []

	for char in message:
		bits = bin(ord(char))[2:]
		bits = '00000000'[len(bits):] + bits
		bit_list.extend([int(bit) for bit in bits])
	filler = 0
	temp_list = bit_list + [filler] * 3
	grouped_list = [temp_list[n:n + 3] for n in range(0, len(bit_list), 3)]

	return grouped_list


def mapping(bits_list, R_):

	co_list = []

	for bits in bits_list:
		if bits == [0, 0, 0]:
			co_list.extend((0, 0))
		elif bits == [0, 0, 1]:
			co_list.extend((0, 1))
		elif bits == [0, 1, 0]:
			co_list.extend((0, -1))
		elif bits == [0, 1, 1]:
			co_list.extend((1, 0))
		elif bits == [1, 0, 0]:
			co_list.extend((1, 1))
		elif bits == [1, 0, 1]:
			co_list.extend((1, -1))
		elif bits == [1, 1, 0]:
			co_list.extend((-1, 0))
		elif bits == [1, 1, 1]:
			co_list.extend((-1, 1))

	return R_(co_list)


def get_num(message, number):

	counter = 0
	m_list = list(message)

	for i in range(len(m_list)):
		if number == m_list[i]:
			counter += 1

	return counter


def decode(grouped_list):

	bit_list = []

	for group in grouped_list:
		bit_list += group

	length = len(bit_list)
	filler_len = length % 8

	if filler_len != 0:
		bit_list = bit_list[:- filler_len]
	message = ''

	for index in range(len(bit_list) // 8):
		byte = bit_list[index * 8: (index + 1) * 8]
		message += chr(int(''.join([str(bit) for bit in byte]), 2))

	return message


def inverse_mapping(co_list):

	bit_list = []

	for co in co_list:
		if co == [0, 0]:
			bit_list.append([0, 0, 0])
		elif co == [0, 1]:
			bit_list.append([0, 0, 1])
		elif co == [0, -1]:
			bit_list.append([0, 1, 0])
		elif co == [1, 0]:
			bit_list.append([0, 1, 1])
		elif co == [1, 1]:
			bit_list.append([1, 0, 0])
		elif co == [1, -1]:
			bit_list.append([1, 0, 1])
		elif co == [-1, 0]:
			bit_list.append([1, 1, 0])
		elif co == [-1, 1]:
			bit_list.append([1, 1, 1])

	return bit_list


def group(ungrouped):

	co_list = []
	for i in range(0, len(ungrouped), 2):
		co_list.append([ungrouped[i], ungrouped[i + 1]])

	return co_list


def mgf(hashed, iterations, R_, N):

	counter = 0

	while counter < iterations:
		hashed = hashing(hashed)
		counter += 1
	counter = 0
	poly_coefs = []

	while counter < N:
		poly_coefs.append(hashed[counter % len(hashed)])
		counter += 1

	return R_(poly_coefs)


def encrypt(message, h, R_, len_b, params):
	print(message+'\n')
	N, q, d1, d2, d3, dg, dm, p = params
	x = R_.gen()
	count_zero = 0
	count_minus = 0
	count_plus = 0
	# the number of +1s,−1s and 0s in m are each≥dm
	while count_zero <= dm or count_minus <= dm or count_plus <= dm:
		# b{0,1}bLen
		b = gen_random_string(len_b)
		salted_message = b + message

		# invertible message formatting function
		# Message×Random bits → TN
		m_prime = mapping(encode(salted_message), R_)
		b_poly = mapping(encode(b), R_)
		# blinding polynomial generation function
		# Message×Random bits×Public key→PN(d1,d2,d3)
		r_prime = mod(((m_prime * b_poly) % (x ** N - 1)) + h, q, R_)
		r = (p * r_prime)
		r = recenter(r, 10, R_)
		r = h * r
		r = r % (x ** N - 1)
		r = mod(r, q, R_)
		r_mod = mod(r, p, R_)
		r_list = r_mod.list()
		if len(r_list) % 2 != 0:
			r_list.append(0)
		r_string = decode(inverse_mapping(group(r_list)))
		# mask generation function
		# RN,q→TN
		mask = mgf(r_string, 20, R_, N)
		m = recenter(m_prime + mask, p, R_)
		count_zero = get_num(m, 0)
		count_minus = get_num(m, -1)
		count_plus = get_num(m, 1)

	secret = r + m

	return secret


def decipher(secret, R_, f, params, h, len_b):

	N, q, d1, d2, d3, dg, dm, p = params
	x = R_.gen()
	a = recenter((secret * f) % (x ** N - 1), q, R_)
	m = recenter(a, p, R_)
	r = secret - m
	r_mod = mod(r, p, R_)
	r_list = r_mod.list()
	if len(r_list) % 2 != 0:
		r_list.append(0)
	r_string = decode(inverse_mapping(group(r_list)))
	# mask generation function
	# RN,q→TN
	mask = mgf(r_string, 20, R_, N)
	# invertible message formatting function
	# Message×Random bits → TN
	m_prime = recenter(m - mask, p, R_)
	m_list = m_prime.list()
	if len(m_list) % 2 != 0:
		m_list.append(0)
	salted_message = decode(inverse_mapping(group(m_list)))
	b = salted_message[:len_b]

	b_poly = mapping(encode(b), R_)
	message = salted_message[len_b:]

	# blinding polynomial generation function
	# Message×Random bits×Public key→PN(d1,d2,d3)
	r_prime = mod(((m_prime * b_poly) % (x ** N - 1)) + h, q, R_)
	new_r = (p * r_prime)
	new_r = recenter(new_r, 10, R_)
	new_r = h * new_r
	new_r = new_r % (x ** N - 1)
	new_r = mod(new_r, q, R_)
	# p·r′∗h=r and the number of +1s,−1s and 0s in m are each≥dm
	if new_r == r:
		print(message)

	return message


if __name__ == '__main__':
	k = 128
	m = 'hello!'
	p = 3
	len_b = 10
	params = param_gen(k)
	params = (*params, 3)
	public_key, private_key, R, _ = create_keys(params)
	secret = encrypt(m, public_key, R, len_b, params)
	msg = decipher(secret, R, private_key[0], params, public_key, len_b)
