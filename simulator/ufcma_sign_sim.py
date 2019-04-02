
from playcrypt.simulator.base_sim import BaseSim


class UFCMASignSim(BaseSim):
    """
    This simulator was written to be used with GameUFCMA. It simulates the
    game with an Adversary and allows you to compute an approximate advantage.
    """

    def run(self):
        """
        Runs the game with the adversary provided to the constructor.

        :return: 1 for success and 0 for failure.
        """
        self.game.initialize()
        return self.game.finalize(self.adversary(self.game.sign))

    def compute_success_ratio(self, n=1000):
        """
        Runs the game n times and computes the ratio of successful runs
        over total runs.

        :return: successes / total_runs
        """
        results = []
        for i in range(0, n):
            results += [self.run()]

        successes = float(results.count(1))
        failures = float(results.count(0))

        return successes / (successes + failures)

    def compute_advantage(self, n=1000):
        """
        Adv = Pr[UFCMA => True]

        :return: Approximate advantage computed using the above equation.
        """

        return self.compute_success_ratio(n)
