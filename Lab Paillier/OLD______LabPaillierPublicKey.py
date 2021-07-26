# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 10:47:21 2021

@author: madma
"""

from phe import PaillierPublicKey
import random
import math

class LabPaillierPublicKey(PaillierPublicKey):
    def lab_encrypt_encoded(self, message_encoded, label, seed):
        
       mask = int(seed, 2)*label*random.randint(10**40)
       message_obfuscated = abs(message_encoded - mask)
       label_encrypted = self.encrypt(mask)
       encrypted_number = EncryptedNumber(self, message_obfuscated, label_encrypted, encoding.exponent)
       return encrypted_number
   