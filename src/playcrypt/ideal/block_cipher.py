from playcrypt.primitives import *

class BlockCipher():
    """
    This class simulates a block cipher. It can emulate a block cipher
    with any key or message size (in bytes).

    Example Usage:

    .. testcode::

        from playcrypt.primitives import *
        from playcrypt.ideal.block_cipher import BlockCipher

        b = BlockCipher(16, 12)
        key = random_string(16)
        cipher_text = b.encrypt(key, "Hello World!")
        decrypted_message = b.decrypt(key, cipher_text)

        print decrypted_message

    .. testoutput::

        Hello World!
    """
    def __init__(self, key_len, block_len):
        """
        :param key_len: Key length for block cipher in bytes.
        :param block_len: Block length for block cipher in bytes.
        """
        self.key_len, self.block_len = key_len, block_len
        self.messages = {}
        self.ciphers = {}

    def encrypt(self, key, block):
        """
        This is a simulated encryption function. Simply use a key and message
        with the proper block length.

        :param key: Key to use for simulated encryption, so this must be of
        length
                    ``self.key_len``.
        :param block: Message to be encrypted, so this must be of length
                        ``self.block_len``.
        :return: The cipher text for the block or ``None`` if the length
                 parameters are not met.
        """
        if len(key) is not self.key_len:
            raise ValueError("Invalid key length, key length was: " + \
                    str(len(key)) + " should be: " + str(self.key_len) + ".")
        if len(block) is not self.block_len:
            raise ValueError("Invalid block length, block length was: " + \
                  str(len(block)) + " should be: " + str(self.block_len) + ".")

        if not (key, block) in self.ciphers:
            cipher = self._new_element(key, self.messages)
            self.ciphers[(key, block)] = cipher
            self.messages[(key, cipher)] = block

        return self.ciphers[(key, block)]

    def decrypt(self, key, cipher):
        """
        This is a simulated decryption function. Use of the correct key and
        cipher text will result in correct decryption. The cipher and key must
        have correct lengths.

        :param key: Key to use for simulated decryption, this must be of length,
                    ``self.key_len``.
        :param cipher: Cipher text to be decrypted, this must be of length
                       ``self.block_len``.
        :return: The correct message for the cipher text, cipher, or
        ``None`` if parameters are not met.
        """
        if len(key) is not self.key_len:
            raise ValueError("Invalid key length, key length was: " + \
                    str(len(key)) + " should be: " + str(self.key_len) + ".")
        if len(cipher) is not self.block_len:
            raise ValueError("Invalid block length, block length was: " + \
                  str(len(cipher)) + " should be: " + str(self.block_len) + ".")

        if not (key, cipher) in self.messages:
            message = self._new_element(key, self.ciphers)
            self.messages[(key, cipher)] = message
            self.ciphers[(key, message)] = cipher

        return self.messages[(key, cipher)]

    def _new_element(self, key, l):
        """
        Returns an element that has not yet been picked. We need this function
        because the cipher must be a bijection.

        :param key: Key to index into in list.
        :param l: List of two tuples to generate a new element in.
        :return: An element that is not yet in the list with the given
                 key.
        """
        e = random_string(self.block_len)
        while (key, e) in l:
            e = random_string(self.block_len)

        return e