# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 16:27:37 2021

@author: madma
"""
from phe import paillier, PaillierPublicKey, EncryptedNumber
import random
import math


DEFAULT_KEYSIZE = 2048

def generate_lab_paillier_keypair(private_keyring=None, n_length=DEFAULT_KEYSIZE):
    p = q = n = None
    n_len = 0
    while n_len != n_length:
        p = getprimeover(n_length // 2)
        q = p
        while q == p:
            q = getprimeover(n_length // 2)
        n = p * q
        n_len = n.bit_length()

    public_key = LabPaillierPublicKey(n)
    private_key = PaillierPrivateKey(public_key, p, q)

    if private_keyring is not None:
        private_keyring.add(private_key)

    return public_key, private_key


class LabPaillierPublicKey(PaillierPublicKey):
    def lab_encrypt_encoded(self, message_encoded, label, seed):
        
       mask = int(seed, 2)*label*random.randint(10**40)
       message_obfuscated = abs(message_encoded - mask)
       label_encrypted = self.encrypt(mask)
       encrypted_number = EncryptedNumber(self, message_obfuscated, label_encrypted, encoding.exponent)
       return encrypted_number

class LabEncryptedNumber(EncryptedNumber):
    def __init__(self, public_key, message_obfuscated, label_encrypted, exponent=0):
        super().__init__(public_key, exponent=0)
        self.message_obfuscated = message_obfuscated
        self.label_encrypted = label_encrypted