Intro
*****

What is this?
=============
This is the documentation for the PlayCrypt library used to implement your 
assignments. The hope is that this framework will make it easier for you to
understand theoretical cryptography by transforming theoretical games into 
runnable code. The documentation contains useful information for solving your 
assignments and helps bridge the gap between theoretical pseudocode and runnable
code. If this is your first time using Python you can find many guides on the 
internet, I found `this guide <http://python4java.necaiseweb.org>`_ extremely
helpful when I was new to the language. 

A central component of theoretical cryptography is the idea of a "game". 
These games are formal settings, which resemble APIs, within which an 
adversary can work towards achieving a particular goal. A good adversary has
a "high" advantage. This framework makes the capabilities of the adversaries
easier to understand by documenting them as actual APIs. This makes more clear 
what these games are as well as what quantities are available to the adversary
for exploitation. Further, once you construct an adversary you can use this 
framework to test whether it is correct or not. 

Getting Around
==============
Here is a brief overview of what you can expect from each section of the 
documentation: 

  1. :doc:`Getting Started </quick_start>` has everything you need to get 
     started with PlayCrypt.
  2. :doc:`Conventions </conventions>` for defining cryptography games in Python
     and simulating common pseudocode operations. 
  3. :doc:`Design and Architecture </design_and_architecture>` details the big
     picture overview of the framework. It introduces and explains the concept 
     of a simulator in the context of games. 
  4. The :doc:`Games </playcrypt.games>` and :doc:`Simultaor </playcrypt.simulator>`
     section contain documentation for all the simulator and game classes you 
     will see in this course. While you can find a lot of information in the 
     documentation there is no replacement for reading the code. 
  5. The :doc:`ideal cryptography </playcrypt.ideal>` section covers the
     library that is used to simulate different primitives including block
     ciphers, signature schemes, hash functions, and MACs.

Hopefully you will find the provided documentation to be useful and answer any
question you might have about applying Python in this context or the framework.
