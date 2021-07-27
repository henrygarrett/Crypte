# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 18:41:34 2021

@author: madma
"""
from pathlib import Path
path = str(Path.cwd().parents[1])
import sys
sys.path.append(path + '\\Crypte\\Lab paillier')
import lab_paillier
import gmpy2

x = 6579807688615876475817486*81561841
y = 735368461546681435458143856438146856
print(x * y)
public, private = lab_paillier.generate_lab_paillier_keypair()
x_encrypted = public.lab_encrypt_encoded(x, 98589732, '10101110001010101010101')
y_encrypted = public.lab_encrypt_encoded(y, 32762498, '10101000101110101001001')
#product_label = public.lab_multiply_ciphers(x_encrypted, y_encrypted)
product = private.lab_multiply_decrypt(x_encrypted, y_encrypted, public.lab_multiply_ciphers(x_encrypted, y_encrypted))
print(product)
print(product == x*y)

