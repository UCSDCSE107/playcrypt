import random

from playcrypt.games.game import Game
from playcrypt.primitives import random_string
from playcrypt.ideal.block_cipher import BlockCipher
from playcrypt.tools import *

class GamePaddingOracle(Game):
    """
    This game is used to exploit padding oracles, in order to recover plaintext messages.
    """
    def __init__(self, key_len, blockSize):
        """
        """
        super(GamePaddingOracle, self).__init__()
        self.key_len, self.blockSize = key_len, blockSize
        self.key = ''
        self.block_cipher = None
        self.plaintext = []
        self.ciphertext = []
        self.plaintextBlocks = 0
        self.plaintextLen = 0
        self.padLen = 0

    def initialize(self):
        
        self.ciphertext = []
        self.plaintext = []
        self.key = random_string(self.key_len)
        self.plaintextBlocks = random.randrange(2, 7, 1)
        self.plaintextLen = self.blockSize * self.plaintextBlocks - random.randrange(0,self.blockSize,1)
        self.block_cipher = BlockCipher(self.key_len, self.blockSize)
        self.padLen = self.blockSize * self.plaintextBlocks - self.plaintextLen

        plaintextTmp = random_string(self.plaintextLen)
        if self.padLen == 0:
            self.padLen = self.blockSize
            self.plaintextLen = self.plaintextLen + self.blockSize
            self.plaintextBlocks = self.plaintextBlocks + 1
        for i in range(0, self.padLen):
            plaintextTmp = plaintextTmp + int_to_string(self.padLen)
        self.plaintext = split(plaintextTmp, self.blockSize)
            

        self.ciphertext.append(random_string(self.blockSize))
        for i in range(0, self.plaintextBlocks):
            self.ciphertext.append(self.block_cipher.encode(self.key, xor_strings(self.ciphertext[i], self.plaintext[i])))
                  

    def dec(self, c):
        """
        This decryption oracle attempts to decrypt, and informs the adversary whether or not
        the plaintext has proper decoding. 
        :param c: Ciphertext the adversary wishes to decrypt.
        :return: Either False if decryption would fail, or True if decryption would succeed.
        """
        good = True
        plaintext = xor_strings(self.block_cipher.decode(self.key, c[len(c)-1]), c[len(c)-2])
        lastByte = string_to_int(plaintext[-1:])
        if lastByte == 0:
            return False
        for i in range (1, lastByte):
            if string_to_int(plaintext[-i-1:-i]) != lastByte :
                good = False
        return good 

    def finalize(self, guess, guessType):
        """
        This method is called automatically by the PaddingOracleSim and evaluates a
        guess that is returned by the adversary.

        :param guessType: 0 indicates the adversary is guessing the padding length. In this case, guess is an ineger.
                          1 indicates that the adversary is guessing the last plaintext byte prior to the padding.  
                            In that case, guess contains a 1 byte string.  We exclude the case where the message is block-aligned. 
                          2 indicates that the adversary is guessing the last plaintext byte of the 2nd-to-last plaintext block.                               In that case, guess contains a 1 byte string.
        :return: True if guess is correct, false otherwise.
        """

        if guessType == 0:
            return guess == self.padLen

        if guessType == 1:
            # Exclude case where message is block aligned.  Allow None as a success. 
            if guess == None and self.padLen == self.blockSize:
                return True
            else: 
                return guess == self.plaintext[self.plaintextBlocks-1][-self.padLen-1:-self.padLen]
        
        if guessType == 2:
            return guess == self.plaintext[self.plaintextBlocks-2][-1:]
