"""
    This module implements 1-out-of-2 oblivious transfer. Essentially,
    the garbler inputs to the protocol two messages :code:`m0` and :code:`m1`,
    while the evaluator inputs a single bit :code:`b`. The garbler
    learns nothing from this protocol and the evaluator learns either
    :code:`m0` or :code:`m1` depending on his bit :code:`b`, but not both.
    The OT protocol followed in this module is the following:

        1. The garbler generates an RSA public/private key pair and sends
        the public portion :code:`(e, N)` to the evaluator along with
        two random messages :code:`x0` and :code:`x1`.

        2. The evaluator generates a random :code:`k` and depending on his bit
        :code:`b` sends to the garbler :code:`v = (xb + k ^ e) mod N`.

        3. The garbler computes both :code:`k0 = (v - x0) ^ d mod N` and
        :code:`k1 = (v - x1) ^ d mod N`. One of these will equal :code:`k`,
        but he doesn't know which.

        4. The garbler sends :code:`m0_ = m0 + k0` and :code:`m1_ = m1 + k1`
        to the evaluator.

        5. The evaluator decrypts depending on his bit :code:`mb_ = mb - k`,
        learning only :code:`m0` or :code:`m1`.

"""

import pickle
from new_gabes.label import Label
from random import randint
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


def garbler_ot1(m0, m1, b):
    """
        The OT protocol seen from the point of view of the garbler.
        This includes creating the RSA key pair, generating
        :code:`x0` and :code:`x1`, computing :code:`k0` and :code:`k1`, and
        sending :code:`m0_` and :code:`m1_`. Note that pickling of
        m0 and m1 is done beforehand for it to be possible to send
        :class:`Label` objects.

        :param client: the evaluator's address
        :param bytes m0: the first bytes object (in this case, a label)
        :param bytes m1: the second bytes object (in this case, a label)
    """

    private_key = rsa.generate_private_key(public_exponent=65537,
                                           key_size=512,
                                           backend=default_backend())
    d = private_key.private_numbers().d

    public_key = private_key.public_key()
    n, e = public_key.public_numbers().n, public_key.public_numbers().e

    x0, x1 = [randint(2, n // 2) for _ in range(2)]
    return [x0, x1, n, e, d]
def garbler_ot2(m0, m1, b, x0, x1, v, d, n):
    k0, k1 = [pow((v - x), d, n) for x in (x0, x1)]
    bytes_m0 = pickle.dumps(m0)
    bytes_m1 = pickle.dumps(m1)
    m0 = int.from_bytes(bytes_m0, byteorder='big')
    m1 = int.from_bytes(bytes_m1, byteorder='big')
    return [m0 + k0, m1 + k1, len(bytes_m0), len(bytes_m1)]


def evaluator_ot1(m0, m1, b, n, x0, x1, e):
    """
        The OT protocol seen from the point of view of the evaluator.
        This includes choosing the random :code:`k`, sending
        :code:`v`, and learning either :code:`m0` or :code:`m1`.


        :param sock: the garbler's address
        :param bool b: the evaluator's bit
    """

    k = randint(2, n // 2)
    b = 1
    chosen_x = x1 if b == '1' else x0
    v = (chosen_x + pow(k, e, n)) % n
    return v, k
def evaluator_ot2(m0, m1, b, t0, t1, size_m1, size_m0, k):
    chosen_t = t1 if b == '1' else t0
    chosen_size = size_m1 if b == '1' else size_m0
    m = chosen_t - k
    label = pickle.loads(int.to_bytes(int(m), length=chosen_size, byteorder='big'))
    return label
label1 = Label(1)
label0 = Label(0)
x0, x1, n, e, d = garbler_ot1(label0, label1, 1)
v,k = evaluator_ot1(label0, label1, 1, n, x0, x1, e)
t0, t1, size_m1, size_m0 = garbler_ot2(label0, label1, 1, x0, x1, v, d, n)
print(evaluator_ot2(label0, label1, 1, t0, t1, size_m1, size_m0, k))
print(label1 == evaluator_ot2(label0, label1, 1, t0, t1, size_m1, size_m0, k))
print(label1 == evaluator_ot2(label0, label1, 1, t0, t1, size_m1, size_m0, k))
