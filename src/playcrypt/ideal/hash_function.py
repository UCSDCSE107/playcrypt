from playcrypt.primitives import *
from playcrypt.tools import *

class HashFunction():
    """
    This class simulates a hash function. It can emulate a hash function with
    or without a key and with any key or output length (in bytes).

    Example Usage:

    .. testcode::

        from playcrypt.ideal.hash_function import HashFunction

        h = HashFunction(16)

        h1 = h.hash("Hello World!")
        h2 = h.hash("H3110 W0r1d!")

        print str(h1 != h2 and len(h1) == h.out_len and len(h1) == len(h2))

    .. testoutput::

        True
    """
    def __init__(self, out_len=0, key_len=0, N=0):
        """
        :param out_len: Output length for the hash function in bytes.
        :param key_len: Key length for the hash function in bytes, defaults
                        to 0.
        """
        self.key_len, self.out_len, self.N = key_len, out_len, N
        self.hashes = {}
        self.hashes_int = {}

    def hash(self, message, key=None):
        """
        This is a simulated hashing function. If a key is used then it must have
        the correct key length.

        :param message: Must be a string of length > 0
        :param key: Key used for simulated hashing, must have length
                    ``self.key_len``.
        :return: Hash of message if all parameters are met, ``None`` otherwise.
        """
        if (key is not None and len(key) is not self.key_len):
            raise ValueError("Invalid key length, key length was: " + \
                    str(len(key)) + " should be: " + str(self.key_len) + ".")

        if self.out_len == 0:
            raise ValueError("Invalid output length: length must be nonzero")

        if not (key, message) in self.hashes:
            self.hashes[(key, message)] = random_string(self.out_len)

        return self.hashes[(key, message)]

    def hash_int(self, message):
        """
        This is a simulated hashing function that takes an input in Z_N^* and
        outputs a value in Z_N^*.

        :param message: Must be an integer in Z_N^*
        :return: Hash of message if all parameters are met, ``None`` otherwise.
        """
        if self.N == 0:
            raise ValueError("Invalid modulus: modulus must be nonzero")

        if not in_Z_N_star(message, self.N):
            raise ValueError("Invalid message: message not in Z_N^*.")

        if not message in self.hashes_int:
            self.hashes_int[message] = random_Z_N_star(self.N)

        return self.hashes_int[message]
