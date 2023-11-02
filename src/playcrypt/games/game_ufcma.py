
from playcrypt.games.game import Game
from playcrypt.primitives import random_string


class GameUFCMA(Game):
    """
    This game is meant to test the security of message authentication schemes.
    Adversaries playing this game have access to a tag and verify oracle.
    """
    def __init__(self, _max_queries, _vf_queries, _tag, _verify, key_len, key_gen=None):
        """
        :param _tag: This must be a callable python function that returns
                     message tags and takes in a key and message (key should
                     be of length key_len).
        :param _verify: This must be a callable python function that returns
                        1 when a tag is valid and 0 when it is not. Its
                        parameters should be key, message, and tag.
        :param key_len: This is the length of the key used by the MAC in bytes.
        """
        super(GameUFCMA, self).__init__()
        self.max_queries, self._tag, self._verify, self.key_len = _max_queries, _tag, _verify, key_len
        self.vf_queries = _vf_queries
        self.key = ''
        self.messages = []
        self.key_gen = key_gen

    def initialize(self):
        """
        Initializes the game and resets the state. Called every time you would
        like to play the game again, usually by the simulator class. Resets
        key and internal storage.
        """
        if self.key_gen is None:
            self.key = random_string(self.key_len)
        else:
            self.key = self.key_gen()
        self.messages = []
        self.win = False
        self.vf_attempts = 0

    def tag(self, message):
        """
        This is the tag oracle that the adversary has access to.

        :param message: Message to be tagged.
        :return: Tag of ``message``.
        """
        t = self._tag(self.key, message)
        self.messages += [message]
        return t


    def verify(self, m, t):
        self.vf_attempts += 1
        if m is None or t is None:
            return False
        if m in self.messages:
            raise ValueError("The queried message is already in the set S.")
            return False
        result = self._verify(self.key, m, t)
        if result == 1:
            self.win = True
        return result


    def finalize(self, return_value):
        """
        This method is usually called automatically by the simulator class
        to determine whether or not the adversary won the game.
        :return: True if successful, False otherwise.
        """
        if self.vf_attempts > self.vf_queries:
            raise ValueError("The adversary must make at most " + str(self.vf_queries) + " Verification queries.")
	
        if len(self.messages) > self.max_queries:
            raise ValueError("The adversary must make at most " + str(self.max_queries) + " Tag queries.")

        return self.win
