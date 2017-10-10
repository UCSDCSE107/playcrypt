from crypto.simulator.base_sim import BaseSim


class CTXTSim(BaseSim):
    """
    This simulator was written to be used with GameINTCTXT. It simulates the
    game with an Adversary and allows you to compute an approximate advantage.
    """
    def run(self):
        """
        Runs the game with the adversary provided to the constructor.

        :return: True for success and False for failure.
        """
        self.game.initialize()
        self.adversary(self.game.enc, self.game.dec)
        return self.game.finalize()

    def compute_success_ratio(self, trials=1000):
        """
        Runs the game trials times and computes the ratio of successful runs
        over total runs.

        :return: successes / total_runs
        """
        results = []
        for i in xrange(0, trials):
            results += [self.run()]

        successes = float(results.count(True))
        failures = float(results.count(False))
        return successes / (successes + failures)

    def compute_advantage(self, trials):
        """
        Adv = Pr[UFCMA => True]

        :return: Approximate advantage computed using the above equation.
        """

        return self.compute_success_ratio(trials)