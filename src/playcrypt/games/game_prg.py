import random

from playcrypt.games.game import Game
from playcrypt.primitives import random_string


class GamePRG(Game):
    """
    This game is used to test whether a candidate function is a good
    pseudo-random generator or not. Adversaries playing this game have
    no access to any oracle.
    """
    def __init__(self, prg, input_len, output_len):
        """
        :param prg: This must be a callable python function that takes
                    input, r of length input_len and outputs a string of length 
                    output_len.

        :param input_len: Length of the input (in bytes) of the function
                          that will be used in this game.

        :param output_len: Length of the output (in bytes) of the function
                           that will be used in this game.
        """
        super(GamePRG, self).__init__()
        self.prg = prg
        self.input_len = input_len
        self.output_len = output_len
        self.challenge = None
        self.world = None

    def initialize(self, world=None):
        """
        This is the initialize method and is part of GamePRG as defined in the
        slides. It is called automatically by WorldSim when a game is run.

        :param world: This is an optional parameter that allows the simulator
                      to control which world the game is in. This allows for
                      more exact simulation measurements.
        :return:
        """
        self.seed = random_string(self.input_len)
        if world is None:
            world = random.randrange(0, 2, 1)
        self.world = world
        if (self.world == 1):
            self.challenge = self.prg(self.seed)
        else:
            self.challenge = random_string(self.output_len)
        
    
    def finalize(self, guess):
        """
        This method is called automatically by the WorldSim and evaluates a
        guess that is returned by the adversary.

        :param guess: Which world the adversary thinks it is in, either a 0
                      or 1.
        :return: True if guess is correct, false otherwise.
        """

        return guess == self.world
