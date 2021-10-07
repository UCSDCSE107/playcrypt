Getting Started
***************

You can install the PlayCrypt library from Github using `pip`::

    pip3 install --user git+https://github.com/UCSDCSE107/playcrypt.git

If you prefer, you can install it in a python virtual environment::

    python3 -m venv playcrypt-venv # create the venv
    . playcrypt-venv/bin/activate
    pip install git+https://github.com/UCSDCSE107/playcrypt.git
 
In this case whenever you work on an a playcrypt assignment you'll first need to
activate your venv with `. playcrypt-venv/bin/activate` (note the dot).

Either way, you can test whether you've installed PlayCrypt correctly by opening
a python console and typing `import playcrypt`. If you get a
ModuleNotFoundError, it's not installed (or you forgot to activate your venv).
Also double-check that you're using Python 3 instead of Python 2. (The first
line )

If you're still having trouble installing playcrypt, please make a *PUBLIC* post
on Piazza that includes what you tried, what error message you're getting, your
OS, and your Python version.

Once you've installed playcrypt, you should be able to download the assignment
python files from the course website (once they're released) and run them. For
example::

    user@laptop$ python hw2.py 
    The advantage of your adversary A1 is approximately 0.0
    The advantage of your adversary A3 is approximately 0.0

If using a venv, be sure to activate it first::

    user@laptop$ . playcrypt-venv/bin/activate
    (playcrypt-venv) user@laptop$ python hw2.py
    The advantage of your adversary A1 is approximately 0.0
    The advantage of your adversary A3 is approximately 0.0
