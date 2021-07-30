# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 12:26:20 2021

@author: madma
"""
from pathlib import Path
path = str(Path.cwd().parents[0])#index needs to be set for cwd which will likely be where operators are run not this file
import pickle
import random
import sys
import os

sys.path.append(path + os.sep + 'lab_paillier')

from lab_paillier.lab_paillier import LabEncryptedNumber

class DataDecryption():
    def __init__(self):
        path
        #lab_multiply_ciphers
        
        
    def lab_multiplication(self, intermediary, cipher1, cipher2, CSP):
        public_key = CSP.public_key
        private_key = CSP.key_manager.private_key
        decrypt_intermediary = private_key.decrypt(intermediary) + private_key.decrypt(cipher1.label_encrypted) * private_key.decrypt(cipher2.label_encrypted)
        return_label = random.randint(0,10**40)
        return_intermediary = decrypt_intermediary - return_label
        return_label_encrypted = public_key.encrypt(return_label)
        return_cipher = LabEncryptedNumber(public_key, return_intermediary,return_label_encrypted)
        return return_cipher


    def group_by_count_encoded(self, gbc_vector_masked, data_set_size, CSP):
        public_key = CSP.public_key
        private_key = CSP.key_manager.private_key
        gbc_vector_masked_decrypted = [private_key.lab_decrypt(value) for value in gbc_vector_masked]
        return_vector = []
        for i, value in enumerate(gbc_vector_masked_decrypted):
            return_vector.append([])
            for j in range(data_set_size):
                if j != value:
                    return_vector[i].append(0)
                else:
                    return_vector[i].append(1)
        return_vector_encrypted = [[public_key.lab_encrypt(bit, self.gen_label(),self.local_gen(public_key)[0]) for bit in value] for value in return_vector]
        return return_vector_encrypted
    def local_gen(self, public_key):
        seed = ''
        for _ in range(100):
            seed += str(random.randint(0,1))
        seed_encoded = int(seed,2)
        seed_encrypted = public_key.encrypt(seed_encoded, None)
        return bin(seed_encoded), seed_encrypted
    def gen_label(self):
        label = str(random.randint(1,9))
        for _ in range(29):
            label += str(random.randint(0,9))
        return int(label)