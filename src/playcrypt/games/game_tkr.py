from playcrypt.games.game import Game
from playcrypt.primitives import random_string


class GameTKR(Game):
    """
    This game tests encryption schemes against key recovery attacks. This
    game differs from KR in that you must match the exact target key.

    Adversaries have access to an fn oracle.
    """
    def __init__(self, encrypt, key_len, block_len):
        """
        :param encrypt: This must be a callable python function that takes two
                        inputs, k and x where k is a key of length key_len and
                        x is a message of length block_len.
        :param key_len: Length of the key (in bytes) used in the function that
                        will be tested with this game.

        :param block_len: Length of the block (in bytes) used in the function
                          that will be used in this game.
        """
        super(GameTKR,self).__init__()
        self.encrypt, self.key_len, self.block_len = encrypt, key_len, block_len
        self.key = ''

    def initialize(self):
        """
        This method initializes the game and generates a new key to be called
        by the corresponding simulator class.
        """
        self.key = random_string(self.key_len)

    def fn(self, m):
        return self.encrypt(self.key, m)

    def finalize(self, key_guess):
        """
        Determines whether the game was won or lost, i.e. if the key_guess is
        consistent with all the encryption queries the adversary made.

        :param key_guess: key to check
        :return: True if the key is consistent, False otherwise.
        """

        return key_guess == self.key
