import random

from playcrypt.primitives import random_string
from playcrypt.games.game import Game


class GameLR(Game):
    """
    This game is used as a base game for games that need to determine between
    a left and right encryption. It is useful to determine how well a scheme
    is hiding its data from the adversary.
    """
    def __init__(self, queries, encrypt, key_len, key_gen=None):
        """
        :param encrypt: This must be a callable python function that takes two
                        inputs, k and x where k is a key of length key_len and
                        x is a message.
        :param key_len: Length of the key (in bytes) used in the function that
                        will be tested with this game.

        """
        super(GameLR, self).__init__()
        self.queries, self.encrypt, self.key_len = queries, encrypt, key_len
        self.key = ''
        self.b = -1
        self.key_gen = key_gen

    def initialize(self, b=None):
        """
        This method initializes the game, generates a new key, and selects a
        random world if needed.

        :param b: This is an optional parameter that allows the simulator
                  to control which world the game is in. This allows for
                  more exact simulation measurements.
        """
        if self.key_gen is None:
            self.key = random_string(self.key_len)
        else:
            self.key = self.key_gen()

        if b is None:
            b = random.randrange(0, 2, 1)
        self.b = b
        self.message_pairs = []

    def lr(self, l, r):
        """
        This is an lr oracle. It returns the encryption of either the left or
        or right message. The encryption and message must be of equal length. A
        query for a particular pair is only allowed to be made once.

        :param l: Left message.
        :param r: Right message.
        :return: Encryption of left message in left world and right message in
                 right world. If the messages are not of equal length then
                 ``None`` is returned.
        """
        if (len(l) != len(r)):
            return None

        if (l, r) in self.message_pairs:
            return None

        self.message_pairs += [(l, r)]

        if self.b == 1:
            return self.encrypt(self.key, r)
        else:
            return self.encrypt(self.key, l)

    def finalize(self, guess):
        """
        This method is called automatically by the WorldSim and evaluates a
        guess that is returned by the adversary.

        :param guess: Which world the adversary thinks it is in, either a 0
                      or 1.
        :return: True if guess is correct, false otherwise.
        """
        if len(self.message_pairs) != self.queries:
            raise ValueError("The adversary must make exactly one LR query.")
        return guess == self.b
