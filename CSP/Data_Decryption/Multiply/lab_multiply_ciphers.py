# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 11:11:25 2021

@author: madma
"""
import pickle
import random
import sys
sys.path.append('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Lab paillier')
from lab_paillier import LabEncryptedNumber
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Public_Key\\public_key', 'rb') as public_key_file:
  public_key = pickle.load(public_key_file)
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\CSP\\Key Manager\\private_key', 'rb') as private_key_file:
  private_key = pickle.load(private_key_file)
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\CSP\\Data_Decryption\\Multiply\\lab_multiply_ciphers', 'rb') as AS_multiply_file:
    intermediary, cipher1, cipher2 = pickle.load(AS_multiply_file)
decrypt_intermediary = private_key.decrypt(intermediary) + private_key.decrypt(cipher1.label_encrypted) * private_key.decrypt(cipher2.label_encrypted)
return_label = random.randint(0,10**40)
return_intermediary = decrypt_intermediary - return_label
return_label_encrypted = public_key.encrypt(return_label)
return_cipher = LabEncryptedNumber(public_key, return_intermediary,return_label_encrypted)
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\AS\\Program Executor\\return_cipher_CSP', 'wb') as return_cipher_CSP_file:
  pickle.dump(return_cipher, return_cipher_CSP_file)
        
