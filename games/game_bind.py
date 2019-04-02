from playcrypt.games.game import Game


class GameBIND(Game):
    """
    This game is used to test whether a candidate commitment scheme is binding.
    Adversaries playing this game do not have access to any oracles. However,
    they do have access to a public parameter pi.
    """

    def __init__(self, p, v):
        """
        :param p: Algorithm used to generate pi. This must be a callable
                  python function that generates a public parameter pi that
                  can be used by the adversary and commit/verify functions.
        :param v: Algorithm used to verify commitment. This must be a
                  callable python function that takes a key, commitment,
                  message and random factor as parameters as defined in
                  the commitment scheme slides.
        """
        super(GameBIND,self).__init__()
        self.p, self.v = p, v

    def initialize(self):
        """
        Sets up the public parameter pi using the parameter generation
        algorithm. Called by Simulator class automatically when a game is run.
        """
        self.pi = self.p()

    def finalize(self, args):
        """
        This method determines whether the game was won or lost by checking it
        to see if the adversary was able to construct two (m, k) pairs with the
        same commitment.
        :param args: (c,m0,m1,k0,k1)
        :param c: Target commitment for (m, k) pairs.
        :param m0: Message 1
        :param m1: Message 2
        :param k0: Verification parameter 1
        :param k1: Verification parameter 2
        :return: True on win, False otherwise.
        """
        (c, m0, m1, k0, k1) = args
        v0 = self.v(self.pi, c, m0, k0)
        v1 = self.v(self.pi, c, m1, k1)

        return v0 == 1 and v1 == 1 and m0 != m1

