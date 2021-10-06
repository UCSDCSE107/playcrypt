

class Game(object):
    """
    This class is the superclass for all games. This doesn't do anything
    functional, but it is meant to define the interfaces that are available to
    simulators. Here almost all initialize and finalize signatures are
    defined. This is to help define and enforce common behavior.

    In general Game objects are meant to be combined with simulator objects
    in order to test adversaries.
    """

    def __init__(self):
        pass

    def initialize(self, b=None):
        """
        Sets up any internal state required by the game. This should be made
        such that calling initialize resets all internal state.

        :param b: optional param to indicate world in some games.
        :return:
        """
        pass

    def finalize(self, m1=None, m2=None):
        """
        Finalize method. As per convention in our framework this
        method always returns true when the adversary wins and is false
        otherwise.

        :param m1: Optional param 1 to finalize.
        :param m2: Optional param 2 to finalize.
        :return: Returns anything from init that needs to go to the adversary.
        """
        return

