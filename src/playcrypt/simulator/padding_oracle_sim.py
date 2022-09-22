
from playcrypt.simulator.base_sim import BaseSim


class PaddingOracleSim(BaseSim):
    """
    This simulator was written to be used with GamePaddingOracle. It simulates the game
    with an Adversary and allows you to compute the probability of a correct guess.
    """

    def run(self, guessType):
        """
        Runs the game with a particular guessType.

        :param guessType: 0 indicates the adversary is guessing the padding length. In this case, guess is an ineger.
                          1 indicates that the adversary is guessing the last plaintext byte prior to the padding.  
                            In that case, guess contains a 1 byte string.  We exclude the case where the message is block-aligned. 
                          2 indicates that the adversary is guessing the last plaintext byte of the 2nd-to-last plaintext block.                               In that case, guess contains a 1 byte string.
        :return: True if guess is correct, false otherwise.
        """
        self.game.initialize()
        return self.game.finalize(self.adversary(self.game.ciphertext, self.game.dec, guessType), guessType)

    def compute_success_ratio(self, type, trials=1000):
        """
        Tries game in world and computes the ratio of success / total runs.

        :param type: guess type to compute for.
        :return: successes / total_runs
        """
        results = []
        for i in range(0, trials):
            results += [self.run(type)]

        successes = float(results.count(1))
        failures = float(results.count(0))

        return successes / (successes + failures)

