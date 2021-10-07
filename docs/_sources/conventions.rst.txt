Conventions
***********
Below is a table of conversions between pseudocode and python functions
located in :doc:`playcrypt.tools </playcrypt.tools>` and 
:doc:`playcrypt.primitives </playcrypt.primitives>`. By importing those two
modules you will have access to all of the functions used in the table below.

In our code we use strings to represent cipher and plain text messages. 
This means that we need several custom functions 
in order to perform common pseduocode tasks such as XORing two messages 
together.

.. highlight:: py

===============================================  ==============================
Pseudocode                                       Python function
===============================================  ==============================
EXT-GCD(a, N) → (d, a', N')                      ``egcd(a, b)``
MOD-INV(a, N) → a :sup:`-1`  mod N               ``modinv(a, m)``
s :sub:`1` || s :sub:`2` || ... || s :sub:`n`    ``join(s)`` *
string → int                                     ``string_to_int(s, optional_length)``
⟨x⟩ (int → string)                               ``int_to_string(x)`` 
⟨x⟩ s.t. length of string                        ``int_to_string(x, l)``
<s> + num mod 2 :sup:`size`                      ``add_int_to_string (s,num,size)``
s1 ⊕ s2                                          ``xor_strings(s1, s2)``
string1 || string2                               ``string1 + string2``
⊥                                                ``None``
a mod N                                          ``a % N``
0\ :sup:`n`\                                     ``"\x00" * (n/8)``
1\ :sup:`n`\                                     ``"\xFF" * (n/8)``
R ←$ {0, 1}  \ :sup:`n`\                         ``rand_string(n/8)``
M ∈ D                                            ``M in D``
M ∉ D                                            ``M not in D``
2\ :sup:`n`\                                     ``2**n``
∣s∣                                              ``len(s)``
AES\ :sub:`k`\(m)                                ``AES(k, m)``
AES\ :sup:`-1` :sub:`k` \(m)                     ``AES_I(k, m)``
===============================================  ==============================

\*s is an array of strings
