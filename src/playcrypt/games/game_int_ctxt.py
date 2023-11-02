from playcrypt.games.game import Game
from playcrypt.primitives import random_string


class GameINTCTXT(Game):
    """
    This game tests the integrity of a ciphertext. It is to be used to test
    to see if the decryption algorithm only decrypts authentic messages that
    have been sent by the sender. The Adversary has access to an encryption
    oracle (enc) and a decryption oracle (dec) that it uses to see if it won.
    """
    def __init__(self, required_queries, _vf_queries, encrypt, decrypt, key_len):
        """
        :param encrypt: Encryption function that takes inputs, a key k of
                        key_len length and a message.
        :param decrypt: Decryption function to match encryption function.
        :param key_len: Length of key used by encrypt and decrypt.
        """
        self.required_queries, self._enc, self._dec, self.key_len = required_queries, encrypt, decrypt, key_len
        self.vf_queries = _vf_queries
        self.key = ''
        self.ciphertexts = []

    def initialize(self):
        """
        Initializes key to be used in encryption. Called by simulator to
        reset game state in between runs.
        """
        self.answered_queries = 0
        self.vf_attempts = 0
        self.key = random_string(self.key_len)
        self.ciphertexts = []
        self.win = False

    def enc(self, m):
        """
        Encryption oracle, you can only query for the same message once.

        :param m: Message to be encrypted.
        :return: Cipher text if valid, ``None`` otherwise.
        """
        self.answered_queries += 1
        c = self._enc(self.key, m)
        self.ciphertexts += [c]
        return c

    def verify(self, c):
        self.vf_attempts += 1
        if c in self.ciphertexts:
            return False 
        m = self._dec(self.key, c)
        if m is not None:
            self.win = True
            return True
        return False

    def finalize(self, return_value):
        """
        Method called by simulator to determine if adversary won.

        :return: True if win, False otherwise.
        """
        if self.required_queries < self.answered_queries:
            raise ValueError("The adversary made " + str(self.answered_queries) + " queries to its enc oracle. It is required to make at most " + str(self.required_queries) + " call(s) to enc.")
        if self.vf_attempts > self.vf_queries:
            raise ValueError("The adversary must make at most " + str(self.vf_queries) + " Verification queries.")

        return self.win