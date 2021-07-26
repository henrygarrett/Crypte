# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 11:17:28 2021

@author: madma
"""
import sys
sys.path.append('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Lab paillier')
import lab_paillier 
import pickle
public_key, private_key = lab_paillier.generate_lab_paillier_keypair()
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Public_Key\\public_key','wb') as public_key_file:
    pickle.dump(public_key, public_key_file)
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\CSP\\Key Manager\\private_key', 'wb') as private_key_file:
    pickle.dump(private_key, private_key_file)

x = 90784647389434
y = 93483876948709
cipher1 = public_key.lab_encrypt(x,468298032, '10101010100101')
cipher2 = public_key.lab_encrypt(y,3452869853, '1111010101010')
product = public_key.general_lab_multiplication(cipher1, cipher2)
answer = private_key.lab_decrypt(product)
print(answer)
print(x*y)
print(answer == x*y)
    
    
