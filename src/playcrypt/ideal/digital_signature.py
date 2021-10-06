from playcrypt.primitives import *

class DigitalSignature():
    """
    This class simulates a digital signature scheme. It can simulate a signature
    scheme with any key or tag length (in bytes).

    Example Usage:

    .. testcode::

        from playcrypt.ideal.digital_signature import DigitalSignature

        m = "ABCDEFGH" * 16
        k = "A" * 128

        ds = DigitalSignature(128, 128)

        pk, sk = ds.key_gen()

        c = ds.sign(pk, m)

        print str(ds.verify(sk, m, c))
        print str(ds.verify(pk, m, c))

    .. testoutput::

        True
        False

    """

    def __init__(self, key_len, tag_len):
        """
        :param key_len: Key length for the DS in bytes.
        :param tag_len: Tag length for the DS in bytes.
        """
        self.key_len, self.tag_len = key_len, tag_len
        self.tags = {}
        self.keys = {}


    def key_gen(self):
        """
        :return: Returns a random key for a DS scheme.
        """
        pk = random_string(self.key_len)
        sk = random_string(self.key_len)

        self.keys[pk] = sk

        return pk, sk

    def sign(self, sk, message):
        """
        This is a simulated sign function.

        :param sk: Key for signing, you must use a key of length
                    ``self.key_len``.
        :param message: Message that will be signed, must have length greater
                        than 0.
        :return: Signature of message if parameters are met, ``None`` otherwise.
        """
        if len(sk) is not self.key_len:
            raise ValueError("Invalid key length, key length was: " + \
                    str(len(sk)) + " should be: " + str(self.key_len) + ".")


        if sk not in self.keys:
            self.keys[sk]= random_string(self.key_len)

        if not (sk, message) in self.tags:
            self.tags[(sk, message)] = random_string(self.tag_len)

        return self.tags[(sk, message)]

    def verify(self, pk, message, tag):
        """
        This is a simulated verification function. Checks to see if the tag
        belongs to the passed in message.

        :param pk: Key to use for simulated verification. It must have length
                    ``self.key_len``.
        :param message:  Message to check against tag.
        :param tag: Tag that is being tested to see if it belongs to message.
        :return: True if the tag is correct, false otherwise.
        """
        if tag is None:
            return False

        if pk not in self.keys.values():
            self.keys[random_string(self.key_len)] = pk

        sk = self.keys[pk]

        if (sk, message) not in self.tags:
            self.sign(sk, message)

        return tag == self.tags[((sk, message))]
