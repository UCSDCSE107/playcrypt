import sys
import os

sys.path.append(os.path.abspath(os.path.join('..')))
from playcrypt.simulator.base_sim import BaseSim


class PKELRSim(BaseSim):
    """
    This simulator was written to be used with GameLR. It simulates the game
    with an Adversary and allows you to compute an approximate advantage.
    """

    def run(self, b):
        """
        Runs the game in a specific world.

        :param world: 1 or 0, for different worlds.
        :return: True for success and False for failure.
        """
        pk = self.game.initialize(b)
        return self.game.finalize(self.adversary(self.game.lr, pk))

    def compute_success_ratio(self, b, trials=1000):
        """
        Tries game in world and computes the ratio of success / total runs.

        :param world: Which world to compute for.
        :return: successes / total_runs
        """
        results = []
        for i in range(0, trials):
            results += [self.run(b)]

        successes = float(results.count(True))
        failures = float(results.count(False))

        return successes / (successes + failures)

    def compute_advantage(self, trials=1000):
        """
        Adv = Pr[Right => 1] - Pr[Left => 1]

        :return: Approximate advantage computed using the above equation.
        """

        return self.compute_success_ratio(1, trials) - (1 - self.compute_success_ratio(0, trials))
