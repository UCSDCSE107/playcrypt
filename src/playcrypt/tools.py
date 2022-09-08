from functools import partial
from io import StringIO

import random

try:
    from IPython import embed as debug
except ImportError:
    pass

def egcd(a, b):
    """
    Computes the extended GCD for (a,b). That is, it computes integers x and y
    such that ax + by = gcd(a, b) as well as gcd(a, b).

    :param a: First parameter for GCD.
    :param b: Second parameter for GCD.
    :return:
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y

def modinv(a, m):
    """
    Computes the modular inverse of a mod m.
    http://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python

    :param a: a in a^-1 mod m
    :param m: m in a^-1 mod m
    :return: a^-1 mod m or None if no inverse exists
    """
    g, x, y = egcd(a, m)
    if g != 1:
        return None
    else:
        return x % m


def join(s):
    """
    Turns an array of strings into one string.

    :param s: Array of string to join.
    :return: One string made by connecting all strings in the array.
    """
    return ''.join(s)

def split(s, n=None):
    """
    Split a string into portions of length n. If n is not supplied the
    string is split in half. Some examples:

    .. testcode::

        from playcrypt.tools import split

        print split("ABCDEF", 1)
        print split("ABCDEF", 2)
        print split("ABCDEF")

    .. testoutput::

        ['A', 'B', 'C', 'D', 'E', 'F']
        ['AB', 'CD', 'EF']
        ['ABC', 'DEF']


    :param s: A string
    :param n: the length of string portions
    :return s[]: an array of the portions of s
    """
    if n is None:
        return [s[:len(s) // 2], s[len(s) // 2:]]
    else:
        return [l for l in iter(partial(StringIO(s).read, n), '')]


def string_to_int(s):
    """
    Converts s to an int

    :param s: A string
    :return: The integer representation of the string s.
    """
    x = 0
    for i in range(len(s)):
        x += ord(s[i]) << (len(s)-1 - i) * 8
    return x

def string_to_binary(s):
    ret = ''
    for i in range(len(s)):
        ret = ret+ bin(string_to_int(s[i]))[2:] + '||'
    return ret[:-2]


def int_to_string(x, l=None):
    """
    Converts a number to a string with length l

    :param x: A number between 0 and 2 ** l
    :param l: The length of the string to be returned
    :return: string
    """
    s = ''
    while x != 0:
        char = chr(x & 0xFF)
        x >>= 8
        s = char + s

    if l is None:
        return s
    else:
        return "\x00" * (l - len(s)) + s


def add_int_to_string(s, num, block_size_bytes):
    """
    Adds a number to a string

    :param s: String of length block_size_bytes
    :param num: A number s.t. 0 <= num < block_size_bytes*8
    :param block_size_bytes: Length of s in bytes
    :return: A string
    """
    x = (string_to_int(s) + num) % (2 ** (block_size_bytes*8))
    s = int_to_string(x, block_size_bytes)
    return s


def xor_strings(s1, s2):
    """
    Returns the bitwise XOR of s1 and s2. If len(s1) != len(s2) the resulting
    XOR operation will be the size of the bigger string.

    :param s1: first string in XOR
    :param s2: second string in XOR
    :return: result of bitwise XOR of s1 and s2.
    """

    if len(s1) < len(s2):
        s1 = s1 + ("\x00" * (len(s2) - len(s1)))
    elif len(s2) < len(s1):
        s2 = s2 + ("\x00" * (len(s1) - len(s2)))


    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))


def bitwise_complement_string(s):
    """
    Returns the bitwise complement of s.

    :param s: string obejct to complement
    :return: result of bitwuise complement
    """
    return xor_strings(s, len(s) * "\xFF")

# https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python:_Proved_correct_up_to_large_N
def is_prime(n, _precision_for_huge_n=16):
    def _try_composite(a, d, n, s):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True # n  is definitely composite

    if not hasattr(is_prime, '_known_primes'):
        is_prime._known_primes = [2, 3]
        is_prime._known_primes += [x for x in range(5, 1000, 2) if is_prime(x)]

    if n in is_prime._known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in is_prime._known_primes):
        return False
    d, s = n - 1, 0
    while not (d % 2):
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653:
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467:
        if n == 3215031751:
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321:
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s)
                   for a in is_prime._known_primes[:_precision_for_huge_n])


def prime_between(s, e):
    candidate = random.randint(s, e)

    while not (is_prime(candidate)):
        candidate = random.randint(s, e)

    return candidate

def exp(a, n, N):
	r = 1
	for i in range(n.bit_length() - 1, -1, -1):
		r = ((r*r) * (a if (n >> i) & 0x1 else 1)) % N

	return r % N

def in_Z_N_star(a, N):
    """
    Determines whether a is in Z_n^*.

    :param a: number to be checked
    :param N: N
    :return: Boolean
    """
    if a < 0 or a>=N:
        return False
    return(egcd(a,N)[0] == 1)

def random_Z_N_star(N):
    """
    Returns the a random element in Z_N^*.

    :param N: N
    :return: random element
    """
    candidate = random.randint(1, N-1)

    while not (in_Z_N_star(candidate, N)):
        candidate = random.randint(1, N-1)

    return candidate

def random_Z_N(N):
    """
    Returns the a random element in Z_N.

    :param N: N
    :return: random element
    """
    return random.randint(0, N-1)

def find_generator_Z_N_star(N, pstatements = False):
    """
    Returns a generator of Z_N_star.

    :param N: N
    :return: The generator.
    """

    if N == 2:
        return 1

    if is_prime(N):
        order = N-1
        g = 2
        while g <= N-1:
            i = 2
            curr = (g**2) % N
            works = True
            while i < order:
                if curr == 1:
                    works = False
                    break
                i += 1
                curr = (curr*g) % N
            if works:
                return g
            elif pstatements:
                print ('Not ' + str(g))
            g += 1
    else:
        ZNstar = set([i for i in range(0,N) if in_Z_N_star(i,N)])



        for g in ZNstar:
            S = set([exp(g,i,N) for i in range(0,N)])
            S = set([i for i in S if in_Z_N_star(i,N)])
            if len(S.symmetric_difference(ZNstar)) == 0:
                return g
            if pstatements:
                print ('Not ' + str(g))
        return None
