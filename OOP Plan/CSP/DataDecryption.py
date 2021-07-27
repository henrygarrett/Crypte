# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 12:26:20 2021

@author: madma
"""
from pathlib import Path
path = str(Path.cwd().parents[2])#index needs to be set for cwd which will likely be where operators are run not this file
import pickle
import random
import sys
sys.path.append(path + '\\Crypte\\Lab Paillier')
from lab_paillier import LabEncryptedNumber

class DataDecryption():
    def __init__(self):
        path
        #lab_multiply_ciphers
        
        
    def lab_multiplication(self):
        with open(path + '\\Crypte\\Public_Key\\public_key', 'rb') as public_key_file:
          public_key = pickle.load(public_key_file)
          
        with open(path + '\\Crypte\\CSP\\Key Manager\\private_key', 'rb') as private_key_file:
          private_key = pickle.load(private_key_file)
        with open(path + '\\Crypte\\CSP\\Data_Decryption\\Multiply\\lab_multiply_ciphers', 'rb') as AS_multiply_file:
            intermediary, cipher1, cipher2 = pickle.load(AS_multiply_file)
        decrypt_intermediary = private_key.decrypt(intermediary) + private_key.decrypt(cipher1.label_encrypted) * private_key.decrypt(cipher2.label_encrypted)
        return_label = random.randint(0,10**40)
        return_intermediary = decrypt_intermediary - return_label
        return_label_encrypted = public_key.encrypt(return_label)
        return_cipher = LabEncryptedNumber(public_key, return_intermediary,return_label_encrypted)
        with open(path + '\\Crypte\\AS\\Program Executor\\return_cipher_CSP', 'wb') as return_cipher_CSP_file:
          pickle.dump(return_cipher, return_cipher_CSP_file)
  
  
  

    def group_by_count_encoded(self):
        with open(path + '\\Crypte\\CSP\\Data_Decryption\\Group_By_Count_Encoded\\gbc_vector_masked','wb') as gbc_vector_masked_file:
            gbc_vector_masked = pickle.load(gbc_vector_masked_file)
        with open(path + '\\Crypte\\Public_Key\\public_key', 'rb') as public_key_file:
            public_key = pickle.load(public_key_file)
        with open(path + '\\Crypte\\CSP\\Key Manager\\private_key', 'rb') as private_key_file:
            private_key = pickle.load(private_key_file)
        with open(path + '\\Crypte\\CSP\\Data_Decryption\\Group_By_Count_Encoded\\data_set_size.txt','r') as data_set_size_file:
            data_set_size = int(data_set_size_file.read())
        gbc_vector_masked_decrypted = [private_key.lab_decrypted(value) for value in gbc_vector_masked]
        return_vector = []
        for i, value in enumerate(gbc_vector_masked_decrypted):
            return_vector.append([])
            for j in range(data_set_size):
                if j != value:
                    return_vector[i].append(0)
                else:
                    return_vector[i].append(1)
        return_vector_encrypted = [[public_key.lab_encrypt(bit) for bit in value] for value in return_vector]
        with open(path + '\\Crypte\\AS\\Program Executor\\Operators\\gbce_return_vector_CSP', 'wb') as gbce_return_vector_file:
            pickle.dump(return_vector_encrypted, gbce_return_vector_file)