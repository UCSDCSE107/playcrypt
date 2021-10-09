import random

from Crypto.Cipher import AES as AES_C
from Crypto.PublicKey import RSA

def random_string(length):
    """
    Function to generate a random string of ``length`` bytes.

    :param length: length of string to generate in bytes
    :return: Random string of size length.
    """
    if length < 0: return None
    return ''.join(chr(random.randrange(256)) for _ in range(length))


def random_string_bits(bits):
    """
    Generates a string of ``floor(bits/8)`` size.

    :param bits: How long string should be in bits.
    :return: Random string of bit length ``floor(bits/8)``.
    """
    return random_string((bits // 8))


def AES(k, m):
    """
    Encrypts m with AES in ECB mode.

    :param k: can be 16, 24 or 32 bytes long
    :param m: should be multiple of 128 bits long
    :return: cipher text
    """
    cipher = AES_C.new(k, mode=AES_C.MODE_ECB)
    return cipher.encrypt(bytes(m))


def AES_I(k, m):
    """
    Decrypts m with AES in ECB mode.

    :param k: can be 16, 24 or 32 bytes long
    :param m: should be multiple of 128 bits long
    :return: plaintext
    """
    cipher = AES_C.new(k, mode=AES_C.MODE_ECB)
    return cipher.decrypt(bytes(m))

def rsa_keygen(len):
    """
    RSA keygen algorithm returns a dictionary containing values for
    (n, e, d, p, q).

    :param len: Length of key in bytes that you would like to generate. Must
                be a multiple of 32 bytes and greater than 128 bytes.
    :return: A dictionary containing the standard RSA key components
             (n - modulo, e - encryption exponent, d - decryption exponent,
             p - first factor of n, q - second factor of n).
    """
    r = RSA.generate(len * 8)

    return {'n': getattr(r.key, 'n'),
            'e': getattr(r.key, 'e'),
            'd': getattr(r.key, 'd'),
            'p': getattr(r.key, 'p'),
            'q': getattr(r.key, 'q')}
