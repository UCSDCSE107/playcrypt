from playcrypt.simulator.base_sim import BaseSim


class PrivKCPASim(BaseSim):
    """
    This simulator was written to be used with GameCCA. It simulates the
    game with an Adversary and allows you to compute an approximate advantage.
    """

    def __init__(self, game, adv, probCorrect=None) : 
        super(PrivKCPASim, self).__init__(game, adv)
        self.probCorrect = probCorrect

    def run(self, b):
        """
        Runs the game in a specific world.

        :param world: 1 or 0, for different worlds.
        :return: True for success and False for failure.
        """
        self.game.initialize(b)
        return self.game.finalize(self.adversary(self.game.lr, self.game.enc_query))

    def compute_success_ratio(self, b, trials=1000):
        """
        Tries game in world and computes the ratio of success / total runs.

        :param world: Which world to compute for.
        :return: successes / total_runs
        """
        results = []
        for i in range(0, trials):
            results += [self.run(b)]

        successes = results.count(True)
        failures = results.count(False)
        return successes/(successes + failures)

    def compute_advantage(self, trials):
        """
        Adv = Pr[Right => 1] - Pr[Left => 1]
 
        Unless probCorrect == True
        Adv = Pr[guess = challenge] 
        :return: Approximate advantage computed using the above equation.
        """

        if self.probCorrect == True :
            return .5*self.compute_success_ratio(1,trials) +  .5 * self.compute_success_ratio(0,trials)
        else : 
            return self.compute_success_ratio(1,trials) - (1 - self.compute_success_ratio(0,trials))
