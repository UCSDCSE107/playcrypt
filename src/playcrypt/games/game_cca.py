from playcrypt.games.game_lr import GameLR


class GameCCA(GameLR):
    """
    This game is used to test whether or not encryption schemes are secure
    under a chosen cipher text attack. Adversaries playing this game have acces
    to an lr(l, r) and dec oracle.
    """
    def __init__(self, encrypt, decrypt, key_len, block_len):
        """
        :param encrypt: This should be a function that takes a key and
                        plaintext as parameters and returns a cipher text.
                        It should take keys of ``key_len`` as its key.
        :param decrypt: This should be a function that takes a key and plain
                        cipher text as parameters and returns the plain text
                        message. It should accept a key of length ``key_len``
                        for its key length.
        :param key_len: Length of key in bytes used by ``encrypt`` and
                        ``decrypt``.
        :param block_len: Length of block size in bytes used by ``encrypt`` and
                        ``decrypt``.
        """
        super(self.__class__, self).__init__(encrypt, key_len, block_len)
        self.decrypt = decrypt
        self.c_list = []

    def lr(self, l, r):
        """
        This is an lr oracle. It returns the encryption of either the left or
        or right message that must be of equal length. A query for a
        particular pair is only allowed to be made once.

        :param l: Left message.
        :param r: Right message.
        :return: Encryption of left message in left world and right message in
                 right world. If the messages are not of equal length then
                 ``None`` is returned.
        """
        c = super(GameCCA, self).lr(l, r)
        self.c_list.append(c)
        return c

    def dec(self, c):
        """
        This is a decryption oracle. The adversary can query to decrypt any
        cipher text that it did not receive from the lr oracle.

        :param c: Cipher text to decrypt.
        :return: Decryption of cipher text if valid. None otherwise.
        """

        if c in self.c_list:
            return None
        return self.decrypt(self.key, c)
