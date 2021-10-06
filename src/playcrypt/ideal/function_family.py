from playcrypt.primitives import *

class FunctionFamily():
    """
    This class simulates a family of functions. It can emulate a family of functions
    with any key, input, and output size (in bytes).

    Example Usage:

    .. testcode::

        from playcrypt.primitives import *
        from playcrypt.ideal.function_family import FunctionFamily

        b = FunctionFamily(16, 12, 10)
        key = random_string(16)
        y = b.evaluate(key, "Hello World!")


    .. testoutput::

    """
    def __init__(self, key_len, input_len, output_len):
        """
        :param key_len: Key length for function family in bytes.
        :param input_len: Input length for function family in bytes.
        :param output_len: Output length for function family in bytes.
        """
        self.key_len, self.input_len, self.output_len = key_len, input_len, output_len
        self.outputs = {}

    def evaluate(self, key, input):
        """
        This is a simulated evaluation function. Simply use a key and input
        with the proper length.

        :param key: Key to use for simulated evaluation, so this must be of
        length
                    ``self.key_len``.
        :param input: Input to evaluation, so this must be of length
                        ``self.input_len``.
        :return: The output for the input or ``None`` if the length
                 parameters are not met.
        """
        if len(key) is not self.key_len:
            raise ValueError("Invalid key length, key length was: " + \
                    str(len(key)) + " should be: " + str(self.key_len) + ".")
        if len(input) is not self.input_len:
            raise ValueError("Invalid input length, input length was: " + \
                  str(len(input)) + " should be: " + str(self.input_len) + ".")

        if not (key, input) in self.outputs:
            output = random_string(self.output_len)
            self.outputs[(key, input)] = output

        return self.outputs[(key, input)]
