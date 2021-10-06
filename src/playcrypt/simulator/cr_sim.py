
from playcrypt.simulator.base_sim import BaseSim


class CRSim(BaseSim):

    def run(self):
        """
        Runs the game with the adversary provided to the constructor.

        :return: True for success and False for failure.
        """
        key = self.game.initialize()
        return self.game.finalize(self.adversary(key))

    def compute_success_ratio(self, trials):
        """
        Runs the game trials times and computes the ratio of successful runs
        over total runs.

        :return: successes / total_runs
        """

        results = []
        for i in range(0, trials):
            results += [self.run()]

        successes = float(results.count(True))
        failures = float(results.count(False))

        return successes / (successes + failures)

    def compute_advantage(self, trials=1000):
        """
        Adv = Pr[CR(H,A)->true]

        :return: Approximate advantage computed using the above equation.
        """

        return self.compute_success_ratio(trials)
