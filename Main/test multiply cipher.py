# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 10:32:27 2021

@author: Garret_H
"""
from phe import PaillierPublicKey, EncryptedNumber, PaillierPrivateKey
pk = PaillierPublicKey(227*97)
sk = PaillierPrivateKey(pk, 227, 97)
#3 is the first message with 2 as it's fixed mask(for now)
m1 = 2
a1, b1 = 3 + m1, EncryptedNumber(pk, (pk.n * m1 + 1) % pk.nsquare)
#3 is the first message with 2 as it's fixed mask(for now)
m2 = 1
a2, b2 = 2 + m2, EncryptedNumber(pk, (pk.n * m2 + 1) % pk.nsquare)
print('n: ' + str(pk.n))
print('n^2: ' + str(pk.nsquare))





part1 = EncryptedNumber(pk, (pk.n * a1*a2 + 1) % pk.nsquare)
print(sk.decrypt(part1) == a1*a2)

part2 = EncryptedNumber(pk,b1._raw_mul(a2))
print(sk.decrypt(part2) == m1*a2)

part3 = EncryptedNumber(pk, b2._raw_mul(a1))
print(sk.decrypt(part3) == m2*a1)





product_label = part1 - part2 - part3
print(sk.decrypt(product_label) == a1*a2 - m1*a2 - m2*a1)
product = sk.decrypt(product_label) + sk.decrypt(b1) * sk.decrypt(b2)
print(sk.decrypt(product_label))
print(sk.decrypt(b1))
print(sk.decrypt(b2))
print(product)
print(product == 6)