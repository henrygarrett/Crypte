# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 18:41:34 2021

@author: madma
"""

import sys
sys.path.append('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Lab paillier')
import lab_paillier

x = 98724987429
print(x)
public, private = lab_paillier.generate_lab_paillier_keypair()
x_encrypted = public.lab_encrypt_encoded(x, 98589732, '10101110001010101010101')
print(x_encrypted)
x_encrypted_decrypted = private.lab_decrypt(x_encrypted)
print(x_encrypted_decrypted)

#RETURNS NEGATIVE OF INPUT PROBABLY DUE TO MODULUS IN ENCRYPT SORT AS NEEDS NON NEGATIVE
