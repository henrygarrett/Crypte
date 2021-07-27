# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 16:30:35 2021

@author: madma
"""
from pathlib import Path
path = str(Path.cwd().parents[3])
import pickle
with open(path + '\\Crypte\\CSP\\Data_Decryption\\Group_By_Count_Encoded\\gbc_vector_masked','wb') as gbc_vector_masked_file:
    gbc_vector_masked = pickle.load(gbc_vector_masked_file)
import sys
sys.path.append(path + '\\Crypte\\Lab paillier')
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