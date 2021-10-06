
class BaseSim():
    """
    This is the base simulator class that all simulators inherit from. It has
    the base constructor which all simulators use.
    """
    def __init__(self, game, adversary):
        """
        :param game: This is the specific instantiation of the game you wish to
                     perform a simulation of.
        :param adversary: This is the adversary you would like to run against
        the game.
        """
        self.game = game
        self.adversary = adversary

