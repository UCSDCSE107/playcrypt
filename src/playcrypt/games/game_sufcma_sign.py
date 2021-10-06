
from playcrypt.games.game import Game
from playcrypt.primitives import random_string


class GameSUFCMASign(Game):
    """
    This game is meant to test the security of digital signature schemes.
    Adversaries playing this game have access to a Sign oracle.
    """
    def __init__(self, _sign, _verify, key_len, key_gen=None):
        """
        :param _sig: This must be a callable python function that returns
                     signatures and takes in a secret key and message (key
                     should be of length key_len).
        :param _verify: This must be a callable python function that returns
                        1 when a signature is valid and 0 when it is not. Its
                        parameters should be public key, message, and signature.
        :param key_len: This is the length of the keys in bytes.
        """
        super(GameSUFCMASign, self).__init__()
        self._sign, self._verify, self.key_len = _sign, _verify, key_len
        self.pk = ''
        self.sk = ''
        self.queries = []
        self.key_gen = key_gen

    def initialize(self):
        """
        Initializes the game and resets the state. Called every time you would
        like to play the game again, usually by the simulator class. Resets
        keys and internal storage.
        """
        if self.key_gen is None:
            self.pk = random_string(self.key_len)
            self.sk = random_string(self.key_len)
        else:
            self.pk, self.sk = self.key_gen()
        self.queries = []
        self.win = False

    def sign(self, message):
        """
        This is the sign oracle that the adversary has access to.

        :param message: Message to be signed.
        :return: Signature of ``message``.
        """
        s = self._sign(self.sk, message)
        self.queries += [(message, s)]
        return s

    def finalize(self, input):
        """
        This method is usually called automatically by the simulator class
        to determine whether or not the adversary won the game.

        :return: True if successful, False otherwise.
        """
        if input is None:
            return False

        (message, signature) = input

        if message is None or signature is None:
            return False

        d = self._verify(self.pk, message, signature)
        if (message, signature) not in self.queries and d == 1:
            self.win = True
        return self.win
