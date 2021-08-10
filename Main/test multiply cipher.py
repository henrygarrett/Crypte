# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 10:32:27 2021

@author: Garret_H
"""
from phe import PaillierPublicKey, EncryptedNumber, PaillierPrivateKey
pk = PaillierPublicKey(227*97)
sk = PaillierPrivateKey(pk, 227, 97)
#3 is the first message with 20 as it's fixed mask(for now)
a1, b1 = 3 + 20, EncryptedNumber(pk, (pk.n * 20 + 1) % pk.nsquare)
#4 is the first message with 100 as it's fixed mask(for now)
a2, b2 = 4 + 100, EncryptedNumber(pk, (pk.n * 100 + 1) % pk.nsquare)
print('n: ' + str(pk.n))
print('n^2: ' + str(pk.nsquare))





part1 = pk.encrypt(a1*a2)
print(sk.decrypt(part1) == a1*a2)

part2 = EncryptedNumber(pk,(b1._raw_mul(a2)))
print(sk.decrypt(part2) == sk.decrypt(EncryptedNumber(pk,(b1._raw_mul(a2)))))

part3 = EncryptedNumber(pk, (b2._raw_mul(a1)))
print(sk.decrypt(part3) == sk.decrypt(EncryptedNumber(pk,(b2._raw_mul(a1)))))





product_label = part1._add_encrypted(part2)._add_encrypted(part3)
#print(product_label)
product = sk.decrypt(product_label) + sk.decrypt(b1) * sk.decrypt(b2)
print(product)
print(product == 12)