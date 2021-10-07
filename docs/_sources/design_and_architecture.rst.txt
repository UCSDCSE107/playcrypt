Design and Architecture
***********************

Before you dive deeper into the Framework, we'd like to explain some of our 
thinking behind its design and how the different pieces work together.

Games
=====
In formal cryptoraphy there is this idea of a "game". A game is a way to think
about playcrypt.raphic schemes in a formal setting. Generally games have a way to 
start and end and indicate a win or lose finishing state. You challenge games
using Adversaries which have a goal of finishing the game in the winning state.
Games also frequently expose "oracles" which are functions that the Adversary
can query to simulate knowledge an Adversary might obtain in the real world. 

In order to approximate these games we have built a Python class for each game 
type. The classes mirror the behavior and formal definition of their 
corresponding formal games as closely as possible. However, there are some
things that the formal games do not have to worry about that we do. For
example, the constructors for our games typically take length parameters for
key or block generation that might be needed by the game. This peculiarity
and much more is documented extensively in the class documentation for the
games which can be found :doc:`here </playcrypt.games>`.

Simulators
==========
Because our games mirror their theoretical counterparts they do not include 
the ability to run themselves. As such we have created the notion of a 
simulator for a game. Each of our game classes have corresponding simulator
classes which can be used to "run" a game. In general simulator constructors
take a game and an adversary as parameters. From there you can perform any 
number of runs of that adversary, all games are built to clean up state between
runs, and thus to run a game again you just call the ``run`` method on the 
simulator. Furthermore, all simulators have a method that can approximate the
advantage that the adversary, which is passed in as a parameter, has against
that particular instance of the game (this is the ``compute_advantage``
method). For more information about simulators see the
:doc:`documentation for the simulator classes </playcrypt.simulator>`.

Assignments
===========
To complete an assignment, you must fill in all of the required functions.
For most assignments that means only filling in the adversary, but some
assignments have more than one function to implement. 

Here is what the layout of most assignments look like: 

- Imports 
- Problem statement and definitions
- Your Adversary 
- Boiler plate main/tester

Pay special attention the the problem statement and adversary. The adversary 
will usually contain in-line documentation of the adversary's parameters and 
expected return.

You can use the :doc:`conventions page </conventions>`  as a reference for how 
to do common pseudo-code operations in Python. Also be sure to check out 
:doc:`playcrypt.tools </playcrypt.tools>` and 
:doc:`playcrypt.primitives </playcrypt.primitives>`.

Ideal Cryptography Library
==========================
In addition to creating game and simulator classes we have also created an 
additional set of tools that instructors can use to create assignments. These
tools allow instructors to simulate ideal versions of several playcrypt.raphic
primitives. We call this set of tools our "Ideal Cryptography Library".
Currently we include classes which simulate 
:mod:`block ciphers <playcrypt.ideal.block_cipher>`,
:mod:`hash functions <playcrypt.ideal.hash_function>`,
:mod:`message authentication codes <playcrypt.ideal.message_authentication_code>`, and
:mod:`digital signature schemes <playcrypt.ideal.digital_signature>`.

