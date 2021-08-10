# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 09:51:30 2021

@author: madma
"""

import pathlib
import pickle
import os
import ast
import numpy as np
import time

from CSP.CryptographicServiceProvider import CryptographicServiceProvider
from AS.AnalyticsServer import AnalyticsServer

def init_crypte(ask_prompt=True, verbose=True):

    if (not ask_prompt) or (input('Replace budget, keys and data? y/n\n') != 'y'):
        generate_keys = False
        if 'budget.txt' not in os.listdir('..' + os.sep + 'CSP'):
            print('There is no version so will create new budget, keys and data')
            generate_keys = True
        with open('..' + os.sep + 'CSP' + os.sep + 'budget.txt', 'r') as budget_file:
            privacy_budget = int(budget_file.read())
    else:
        privacy_budget = input('What is the privacy budget?: ')
        generate_keys = True

    CSP = CryptographicServiceProvider(privacy_budget, generate_keys)
    AS = AnalyticsServer(CSP.key_manager.public_key)

    if generate_keys:
        # Creates then encodes then encrypts the data
        AS.aggregator.get_data()
        AS.aggregator.encode_data()
        AS.aggregator.encrypt_data()
    else:
        # Retrieves encrypted data and raw data
        with open('..' + os.sep + 'Main' + os.sep + 'data_set.txt', 'r') as data_file:
            AS.aggregator.data = ast.literal_eval(data_file.read())

        with open('..' + os.sep + 'Main' + os.sep + 'encrypted_data', 'rb') as data_file:
            AS.aggregator.data_encrypted = pickle.load(data_file)

    if verbose:
        print("\nDisplaying initialised Crypte objects...")
        print("\t" + str(AS))
        print("\t" + str(CSP))
        print("\n")
    return AS, CSP

# Initialise Crypte system

AS, CSP = init_crypte(ask_prompt=False)

# Raw data for the tests
TEST_DATA = [['25', 'spain', 'yes'], ['38', 'france', 'no'], ['39', 'italy', 'no'], ['29', 'italy', 'yes'], ['22', 'italy', 'yes']]

# Test functions

# Tests that the aggregator correctly encodes and decodes data to and from one-hot vector form
def test_encode_decode(verbose=True):
    decoded_data = AS.aggregator.decode_row(AS.aggregator.data_encoded[0])
    decoded_data = [str(val) for val in decoded_data]
    raw_data = [str(val) for val in AS.aggregator.data[0]]

    if verbose:
        print("Decoded Data:" + str(decoded_data))
        print("Raw Data:" + str(raw_data))
        print("Test Result:", str(decoded_data == raw_data))
        print("\n")

    assert decoded_data == raw_data

def test_encrypt_decrypt(verbose=True):


    decrypted_data = int(CSP.key_manager.private_key.lab_decrypt(CSP.key_manager.public_key.lab_encrypt(10,47, '10101010')))
    raw_data = 10
    if verbose:
        print("Decrypted Data:" + str(decrypted_data))
        print("Raw Data:" + str(raw_data))
        print("Test Result:", str(decrypted_data == raw_data))
        print("\n")

    assert decrypted_data == raw_data
def test_multiply_ciphers(CSP):
    cipher1 = CSP.key_manager.public_key.lab_encrypt(47846845, CSP.gen_label(), CSP.local_gen(CSP.key_manager.public_key)[0])
    cipher2 = CSP.key_manager.public_key.lab_encrypt(45879457845, CSP.gen_label(), CSP.local_gen(CSP.key_manager.public_key)[0])
    result = CSP.key_manager.private_key.lab_multiply_decrypt(cipher1, cipher2, CSP.key_manager.public_key.multiply_ciphers(cipher1, cipher2, CSP))
    print(result)
    assert result == 47846845 * 45879457845
    print(result == 47846845 * 45879457845)
# Tests general LabHE multiplication
def test_HE_mult():
    ciphertext1 = CSP.key_manager.public_key.lab_encrypt(47846845, CSP.gen_label(), CSP.local_gen(CSP.key_manager.public_key)[0])
    ciphertext2 = CSP.key_manager.public_key.lab_encrypt(45879457845, CSP.gen_label(), CSP.local_gen(CSP.key_manager.public_key)[0])
    
    result = CSP.key_manager.public_key.general_lab_multiplication(ciphertext1, ciphertext2, CSP)
    decrypted_result = CSP.key_manager.private_key.lab_decrypt(result)
    print(decrypted_result)
    assert decrypted_result == 47846845 * 45879457845
    print(decrypted_result == 47846845 * 45879457845)
    

# Tests the Project Operator works correctly
def test_project(verbose=True):

    # Compute test query
    query_result = AS.aggregator.decode_data(CSP.decrypt_data(AS.program_executor.project(AS.aggregator.data_encrypted, [0,2])), attribute_nums=[0,2]) # project, decrypt, decode
    query_result = list(map(lambda x: [str(val) for val in x], query_result)) # Raw data is strings so this is just to make the assert comparison work at the end

    # Get the actual filtering answer
    data = AS.aggregator.data.copy()
    filtered_raw_data = []

    for row in data:
        filtered_row = []
        for i, val in enumerate(row):
            if i in [0,2]:
                filtered_row.append(val)
        filtered_raw_data.append(filtered_row)

    if verbose:
        print("True Filtered Data:", query_result)
        print("Query Result:", filtered_raw_data)
        print("Test Result:", str(filtered_raw_data == query_result))
        print("\n")

    assert filtered_raw_data == query_result

def test_count(verbose=True):
    bit_vector = [1,0,0,1,1]

    # Encrypted bit_vector
    bit_vector_enc = [CSP.key_manager.public_key.lab_encrypt(val, AS.aggregator.gen_label(), AS.aggregator.local_gen(CSP.key_manager.public_key)[0]) for val in bit_vector]

    query_result = CSP.key_manager.private_key.lab_decrypt(AS.program_executor.count(bit_vector_enc)) # Count the bit_vector, decrypt

    assert query_result == 3

# Tests the Filter operator works correctly
def test_filter():
    bit_vector = AS.program_executor.filter(AS.aggregator.data_encrypted, [list(np.ones(21, dtype="uint8")), [1,1,1,1,1],[1,0]], CSP)
    print("Decrypted filter:", CSP.decrypt_bit_vector(bit_vector))

#test_multiply_ciphers(CSP)
#test_encrypt_decrypt()
#test_encode_decode()
test_HE_mult()
# test_project()
# test_count()
# test_filter()
