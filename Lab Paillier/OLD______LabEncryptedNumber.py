# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 10:23:35 2021

@author: madma
"""
from phe import EncryptedNumber
class LabEncryptedNumber(EncryptedNumber):
    def __init__(self, public_key, message_obfuscated, label_encrypted, exponent=0):
        super().__init__(public_key, exponent=0)
        self.message_obfuscated = message_obfuscated
        self.label_encrypted = label_encrypted
    