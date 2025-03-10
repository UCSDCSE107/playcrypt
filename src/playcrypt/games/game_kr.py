from playcrypt.games.game import Game
from playcrypt.primitives import random_string


class GameKR(Game):
    """
    This game tests encryption schemes against key recovery attacks. In order to
    win in this instantiation of KR you must make at least one oracle query.
    Adversaries have access to an fn oracle.
    """
    def __init__(self, queries, encrypt, key_len, block_len):
        """
        :param encrypt: This must be a callable python function that takes two
                        inputs, k and x where k is a key of length key_len and
                        x is a message of length block_len.
        :param key_len: Length of the key (in bytes) used in the function that
                        will be tested with this game.

        :param block_len: Length of the block (in bytes) used in the function
                          that will be used in this game.
        """
        super(GameKR,self).__init__()
        self.queries, self.encrypt, self.key_len, self.block_len = queries, encrypt, key_len, block_len
        self.key = ''
        self.count = 0
        self.messages = {}
        self.ciphertexts = {}
        pass

    def initialize(self):
        """
        This method initializes the game and generates a new key to be called
        by the corresponding simulator class.
        """
        self.key = random_string(self.key_len)
        self.count = 0
        self.messages = {}
        self.ciphertexts = {}

    def fn(self, m):
        self.messages[self.count] = m
        self.ciphertexts[self.count] = self.encrypt(self.key, m)
        self.count += 1
        return self.ciphertexts[self.count-1]

    def finalize(self, key_guess):
        """
        Determines whether the game was won or lost, i.e. if the key_guess is
        consistent with all the encryption queries the adversary made.

        :param key_guess: key to check
        :return: True if the key is consistent, False otherwise.
        """
        if self.count is 0:
            return False

        win = True
        for i in range(self.count):
            if self.encrypt(key_guess, self.messages[i]) != self.ciphertexts[i]:
                win = False
            for j in range(i):
                if self.messages[i] == self.messages[j]:
                    win = False
        if self.count != self.queries:
            win = False
            print(f"Warning: The adversary was supposed to make exactly {self.queries} queries, but instead it made {self.count}. Setting win = False.")
        return win
