import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join('..')))
from playcrypt.primitives import random_string
from playcrypt.games.game import Game

class GameINDCPAIBE(Game):
    """
    This game is used as a base game for games that need to determine between
    a left and right encryption. It is useful to determine how well a scheme
    is hiding its data from the adversary.
    """
    def __init__(self, max_queries_lr, max_queries_exp, p, k, e):
        super(GameINDCPAIBE, self).__init__()
        self.max_queries_lr, self.max_queries_exp = max_queries_lr, max_queries_exp
        self.p, self.k, self.e = p, k, e
        #self.mpk = ''
        #self.msk = ''
        #self.b = -1
        self.warning = ''   

    def initialize(self, b=None):
        if b is None:
            b = random.randrange(0, 2, 1)
        self.b = b
        self.exposed_ids = {}
        self.challenge_ids = {}
        (self.mpk, self.msk) = self.p()       
        return self.mpk

    def lr(self, I, l, r):
        if I in self.exposed_ids:
            return None            
        if (len(l) != len(r)):
            return None			

        self.challenge_ids[I] = True
        if self.b == 1:
            return self.e(self.mpk, I, r)
        else:
            return self.e(self.mpk, I, l)

    def expose(self, I):
        if I in self.challenge_ids:
            return None        
        
        self.exposed_ids[I] = True        
        sk = self.k(self.mpk, self.msk, I)
        return sk
            
    def finalize(self, guess):        
        if len(self.challenge_ids) > 1 or len(self.exposed_ids) > 1:
            self.warning = "Note: the adversary made more oracle queries than allowed."
            guess = random.randrange(0, 2, 1) # Re-randomize the challenge bit to force the loss
            
        res = (guess == self.b)
        return res

    def __del__(self):
        if self.warning != '':
            print (self.warning)