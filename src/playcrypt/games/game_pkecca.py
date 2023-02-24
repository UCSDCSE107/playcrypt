import sys, random
from playcrypt.games.game import Game

class GamePKECCA(Game):
    def __init__(self, min_lr_queries, max_lr_queries, min_dec_queries, max_dec_queries, encrypt, decrypt, k_gen):
        super(GamePKECCA, self).__init__()
        self.min_lr_queries = min_lr_queries
        self.max_lr_queries = max_lr_queries
        self.min_dec_queries = min_dec_queries
        self.max_dec_queries = max_dec_queries
        self.encrypt    = encrypt
        self.decrypt    = decrypt
        self.k_gen      = k_gen
        self.pk = ''
        self.sk = ''
        self.b = -1

    def initialize(self, b=None):
        """
        This method initializes the game, generates a new key, and selects a
        random world if needed.
        :param b: This is an optional parameter that allows the simulator
                  to control which world the game is in. This allows for
                  more exact simulation measurements.
        """
        (self.pk, self.sk) = self.k_gen()
        if b is None:
            b = random.randrange(0, 2, 1)
        self.b = b
        self.message_pairs = []
        self.ciphertexts = []
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

        if (l, r) in self.message_pairs:
            return None
			
        self.message_pairs += [(l, r)]

        if self.b == 1:
            C = self.encrypt(self.pk, r)
            self.ciphertexts += [C]
            return C
        else:
            C = self.encrypt(self.pk, l)
            self.ciphertexts += [C]
            return C

    def dec(self, C):
        if C in self.ciphertexts:
            return None
        
        self.ciphertexts += [C]
        return self.decrypt(self.sk, C)

    def finalize(self, guess):
        """
        This method is called automatically by the WorldSim and evaluates a
        guess that is returned by the adversary.
        :param guess: Which world the adversary thinks it is in, either a 0
                      or 1.
        :return: True if guess is correct, false otherwise.
        """
        
        lr_queries = len(self.message_pairs)
        dec_queries = len(self.ciphertexts) - lr_queries
        if lr_queries < self.min_lr_queries or lr_queries > self.max_lr_queries:
            return False
        if dec_queries < self.min_dec_queries or dec_queries > self.max_dec_queries:
            return False
        return guess == self.b