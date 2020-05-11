import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join('..')))
from playcrypt.primitives import random_string
from playcrypt.games.game import Game
from playcrypt.tools import egcd

class GamePKELR(Game):
    """
    This game is used as a base game for games that need to determine between
    a left and right encryption. It is useful to determine how well a scheme
    is hiding its data from the adversary.
    """
    def __init__(self, min_queries, max_queries, encrypt, pk_gen):
        """
        :param encrypt: This must be a callable python function that takes two
                        inputs, k and x where k is a key of length key_len and
                        x is a message.
        :param key_len: Length of the key (in bytes) used in the function that
                        will be tested with this game.

        """
        super(GamePKELR, self).__init__()
        self.min_queries, self.max_queries, self.encrypt = min_queries, max_queries, encrypt
        self.pk = ''
        self.b = -1
        self.pk_gen = pk_gen
        self.warning = ''

    def initialize(self, b=None):
        """
        This method initializes the game, generates a new key, and selects a
        random world if needed.

        :param b: This is an optional parameter that allows the simulator
                  to control which world the game is in. This allows for
                  more exact simulation measurements.
        """
        self.pk = self.pk_gen()
        if b is None:
            b = random.randrange(0, 2, 1)
        self.b = b
        self.message_pairs = []
        return self.pk

    def lr(self, l, r):
        """
        This is an lr oracle. It returns the encryption of either the left or
        or right message. A query for a particular pair is only allowed to be
        made once.

        :param l: Left message.
        :param r: Right message.
        :return: Encryption of left message in left world and right message in
                 right world. If the messages are not of equal length then
                 ``None`` is returned.
        """
        #if (len(l) != len(r)):
        #    return None

        if (l, r) in self.message_pairs:
            return None

        # New code starts here
        (N, e) = self.pk
        (lg, ly, lx) = egcd(l, N)
        (rg, ry, rx) = egcd(r, N)
        if lg != 1 or rg != 1:
            return None
        # New code ends here			
			
        self.message_pairs += [(l, r)]

        if self.b == 1:
            return self.encrypt(self.pk, r)
        else:
            return self.encrypt(self.pk, l)

    def finalize(self, guess):
        """
        This method is called automatically by the WorldSim and evaluates a
        guess that is returned by the adversary.

        :param guess: Which world the adversary thinks it is in, either a 0
                      or 1.
        :return: True if guess is correct, false otherwise.
        """
        
        queries = len(self.message_pairs)
        if queries < self.min_queries or queries > self.max_queries:
            self.warning = "Note: the adversary lost because it made too few queries or too many queries."
            b = random.randrange(0, 2, 1) # Re-randomize the challenge bit to force the loss
        
        res = (guess == self.b)
        return res

    def __del__(self):
        if self.warning != '':
            raise ValueError(self.warning)