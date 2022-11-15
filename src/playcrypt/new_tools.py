import sys
import os

sys.path.append(os.path.abspath(os.path.join('..')))
from Crypto.Hash import SHA256
from playcrypt.tools import *    
    
def MOD_INV(a,N):
    return modinv(a,N)    
    
def K_rsa(k):
    # Generate N, p, q
    while True:
        # Let p be a prime such that 2**(k/2-1) <= p <= 2**(k/2)
        p = prime_between(2**(k/2-1), 2**(k/2))
        # Let q be a prime such that 2**(k-1) <= p*q <= 2**k
        left = 2**(k-1) // p
        right = 2**k // p
        q = prime_between(left, right)
        N = p * q
        if p != q and 2**(k-1) <= N and N <= 2**k:
            break
    # Generate e, d
    phi = (p - 1) * (q - 1) # phi(N)
    e = random_Z_N_star(phi)
    d = MOD_INV(e, phi)
    return (N, p, q, e, d)
    
def random_string_as_integer(length):
    r = random.randint(0, 2**(length)-1)
    return r

def VOL(j):
    def vol(x, l):
        """
        The variable output length function
        :param x: an int type that represents the input string to hash
        :param l: output length
        :return:  a binary string 
        """
        n = -(l // -256)
        Y = ''
        h = SHA256.new()
        l = l % (2**64)
        h.update(bytes(int_to_string(j,8) + int_to_string(l,8) + int_to_string(x), 'utf-8'))
        P = h.hexdigest()
        for i in range(n):
            i = i % (2**64)
            h.update(bytes(int_to_string(i,8) + P, 'utf-8'))
            Y += h.hexdigest()
        Y = bin(string_to_int(Y))
        return Y[2: l+2]
    return vol