import random

from playcrypt.games.game import Game
from playcrypt.primitives import random_string

class GamePRF(Game):
    """
    This game is used to test whether a candidate function is a good
    pseudo-random function or not. Adversaries playing this game have
    access to an fn oracle.
    """
    def __init__(self, required_queries, prf, key_len, input_len, output_len=None):
        """
        :param prf: This must be a callable python function that takes two
                    inputs, k and x where k is a key of length key_len and x is a
                    message of length input_len.

        :param key_len: Length of the key (in bytes) used in the function that
                        will be tested with this game.

        :param input_len: Length of the input (in bytes) of the function
                          that will be used in this game.

        :param output_len: Length of the output (in bytes) of the function
                           that will be used in this game.
        """
        super(GamePRF, self).__init__()
        self.required_queries, self.prf, self.key_len, self.input_len = required_queries, prf, key_len, input_len
        if output_len == None:
            self.output_len = input_len
        else:
            self.output_len = output_len
        self.key = ''
        self.messages = {}
        self.world = None


    def initialize(self, world=None):
        """
        This is the initialize method and is part of GamePRF as defined in the
        slides. It is called automatically by WorldSim when a game is run.

        :param world: This is an optional parameter that allows the simulator
                      to control which world the game is in. This allows for
                      more exact simulation measurements.
        :return:
        """
        self.answered_queries = 0
        self.messages = {}
        self.key = random_string(self.key_len)
        if world is None:
            world = random.randrange(0, 2, 1)
        self.world = world

    def fn(self, m):
        """
        This is the fn oracle that is exposed to the adversary via the
        simulator. It takes in a message m of length self.input_len and
        returns either the encrypted result in the real world and the
        random result in the random world. 0 = random world, 1 = real world.

        :param m: Message adversary wants to encrypt.
        :return: Either the encrypted result in the real world or random result
                 in the random world.
        """
        if len(m) is not self.input_len:
            raise ValueError("Message is of length " + str(len(m)) + 
                    " but should be " + str(self.input_len) + ".")

        self.answered_queries += 1
        if self.world == 0:
            if m not in self.messages.keys():
                self.messages[m] = random_string(self.output_len)
            return self.messages[m]
        else:
            return self.prf(self.key, m)

    def finalize(self, guess):
        """
        This method is called automatically by the WorldSim and evaluates a
        guess that is returned by the adversary.

        :param guess: Which world the adversary thinks it is in, either a 0
                      or 1.
        :return: True if guess is correct, false otherwise.
        """

        if self.required_queries < self.answered_queries:
            raise ValueError("The adversary made " + str(self.answered_queries) + " queries to its Fn oracle. It is required to make at most " + str(self.required_queries) + " call(s) to Fn.")
        return guess == self.world
