from playcrypt.primitives import random_string
from playcrypt.games.game_lr import GameLR
from playcrypt.ideal.block_cipher import BlockCipher

class GamePrivKCPA(GameLR):
    """
    This game is used to test whether or not encryption schemes are secure
    under a chosen plaintext attack in the private key setting. 
    Adversaries playing this game have access to an enc oracle.
    """
    def __init__(self, queries, encrypt, key_len, key_gen=None):
        """
        :param encrypt: This must be a callable python function that takes two
                        inputs, k and x where k is a key of length key_len and
                        x is a message.
        :param key_len: Length of the key (in bytes) used in the function that
                        will be tested with this game.

        """
        super(self.__class__, self).__init__(1, encrypt, key_len)
            
    def enc_query(self, m):
        return self.encrypt(self.key, m)
        
        
