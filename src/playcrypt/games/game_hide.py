import random

from playcrypt.games.game import Game


class GameHIDE(Game):
    """
    This game is used to test whether a candidate commitment scheme is hiding.
    Compared to game_lr.py, the only difference below is that we allow to query
    oracle lr with the same message pair (l,r) an arbitrary number of times.
    """

    def __init__(self, p, c):
        super(GameHIDE,self).__init__()
        self.p, self.c = p, c
        self.pi = ''
        self.b = -1

    def initialize(self, b=None):
        self.pi = self.p()
        if b is None:
            b = random.randrange(0, 2, 1)
        self.b = b
        return self.pi

    def lr(self, l, r):
        # if (len(l) != len(r)):
        #     return None
        if self.b == 1:
            (C, K) = self.c(self.pi, r)
        else:
            (C, K) = self.c(self.pi, l)
        return C

    def finalize(self, guess):
        return guess == self.b
