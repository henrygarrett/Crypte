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

x = 98724987429
print(x)
public, private = lab_paillier.generate_lab_paillier_keypair()
x_encrypted = public.lab_encrypt_encoded(x, 98589732, '10101110001010101010101')
print(x_encrypted)
x_encrypted_decrypted = private.lab_decrypt(x_encrypted)
print(x_encrypted_decrypted)

