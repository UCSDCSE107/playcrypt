from playcrypt.primitives import *

class MAC():
    """
    This class simulates a message authentication code scheme. It can simulate
    a MAC with any key or tag length (in bytes).

    Example Usage:

    .. testcode::

        from playcrypt.ideal.message_authentication_code import MAC

        m = "ABCDEFGH"
        k = "A" * 16

        mac = MAC(16, 16)

        c = mac.tag(k, m)

        print str(mac.verify(k, m, c))
        print str(mac.verify(k, m, k))

    .. testoutput::

        True
        False
    """
    def __init__(self, key_len, tag_len):
        """
        :param key_len: Key length for the MAC in bytes.
        :param tag_len: Tag length for the MAC in bytes.
        """
        self.key_len, self.tag_len = key_len, tag_len
        self.tags = {}

    def tag(self, key, message):
        """
        This is a simulated tagging function.

        :param key: Key for tagging. You must use a key of length
                    ``self.key_len``.
        :param message: Message that will be tagged. It must have length greater
                        than 0.
        :return: Tag of message if parameters are met, ``None`` otherwise.
        """
        if len(key) is not self.key_len:
            raise ValueError("Invalid key length, key length was: " + \
                    str(len(key)) + " should be: " + str(self.key_len) + ".")

        if not (key, message) in self.tags:
            self.tags[(key, message)] = random_string(self.tag_len)

        return self.tags[(key, message)]

    def verify(self, key, message, tag):
        """
        This is a simulated verification function. Checks to see if the tag
        belongs to the passed in message.

        :param key: Key to use for simulated verification. It must have length
                    ``self.key_len``.
        :param message: Message to check against tag.
        :param tag: Tag that is being tested to see if it belongs to message.
        :return: True if the tag is correct, false otherwise.
        """
        if tag is None:
            return False

        if (key, message) not in self.tags:
            self.tag(key, message)

        return tag == self.tags[((key, message))]

