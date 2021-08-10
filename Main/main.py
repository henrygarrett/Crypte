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
TEST_DATA = [['25', 'spain', 'yes'], ['38', 'france', 'no'], ['39', 'italy', 'no'], ['29', 'italy', 'yes'],
             ['22', 'italy', 'yes']]


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
    return True

def test_encrypt_decrypt(verbose=True):
    decrypted_data = int(CSP.key_manager.private_key.lab_decrypt(CSP.key_manager.public_key.lab_encrypt(10)))
    raw_data = 10
    if verbose:
        print("Decrypted Data:" + str(decrypted_data))
        print("Raw Data:" + str(raw_data))
        print("Test Result:", str(decrypted_data == raw_data))
        print("\n")

    assert decrypted_data == raw_data
    return True


def test_encrypted_data(verbose=True):
    decrypted_data = CSP.decrypt_data(AS.aggregator.data_encrypted)
    if verbose:
        print(AS.aggregator.data_encoded)
        print(decrypted_data)
    assert decrypted_data == AS.aggregator.data_encoded
    return True


def test_multiply_ciphers(CSP):
    cipher1 = CSP.key_manager.public_key.lab_encrypt(47846845)
    cipher2 = CSP.key_manager.public_key.lab_encrypt(45879457845)
    result = CSP.key_manager.private_key.lab_multiply_decrypt(cipher1, cipher2, CSP.key_manager.public_key.multiply_ciphers(cipher1, cipher2, CSP))
    print(result)
    assert result == 47846845 * 45879457845
    return True


# Tests general LabHE multiplication
def test_HE_mult():
    ciphertext1 = CSP.key_manager.public_key.lab_encrypt(47846845)
    ciphertext2 = CSP.key_manager.public_key.lab_encrypt(45879457845)
    
    result = CSP.key_manager.public_key.general_lab_multiplication(ciphertext1, ciphertext2, CSP)
    decrypted_result = CSP.key_manager.private_key.lab_decrypt(result)
    print("Actual Answer:", 47846845 * 45879457845)
    print("Decrypted Result:", decrypted_result)
    assert decrypted_result == 47846845 * 45879457845
    return True


# Tests the Project Operator works correctly
def test_project(verbose=True):

    # Compute test query for projection of 1 attribute
    one_attribute_test = np.array(AS.program_executor.project(AS.aggregator.data_encrypted, 0), dtype="object")

    # Compute test query for projection of > 1 attributes
    query_result = AS.aggregator.decode_data(
        CSP.decrypt_data(AS.program_executor.project(AS.aggregator.data_encrypted, [0, 2])),
        attribute_nums=[0, 2])  # project, decrypt, decode
    query_result = list(map(lambda x: [str(val) for val in x], query_result))  # Raw data is strings so this is just to make the assert comparison work at the end

    # Get the actual filtering answer
    data = AS.aggregator.data.copy()
    projected_raw_data = []

    for row in data:
        filtered_row = []
        for i, val in enumerate(row):
            if i in [0, 2]:
                filtered_row.append(val)
        projected_raw_data.append(filtered_row)

    if verbose:
        print("True Projected Data:", query_result)
        print("Query Result:", projected_raw_data)
        print("Test Result:", str(projected_raw_data == query_result))
        print("One attribute shape:", one_attribute_test.shape)
        print("\n")

    assert projected_raw_data == query_result
    assert one_attribute_test.shape == (5,1,21)
    return True


def test_count(verbose=True):
    bit_vector = [1, 0, 0, 1, 1]

    # Encrypted bit_vector
    bit_vector_enc = [CSP.key_manager.public_key.lab_encrypt(val) for val in bit_vector]

    query_result = CSP.key_manager.private_key.lab_decrypt(AS.program_executor.count(bit_vector_enc)) # Count the bit_vector, decrypt

    if verbose:
        print("Query Result:", query_result)
        print("Actual answer:", 3)
        print("\n")

    assert query_result == 3
    return True


# Tests the Filter operator works correctly
def test_filter(verbose=True):
    bit_vector1 = AS.program_executor.filter(AS.aggregator.data_encrypted, [list(np.ones(21, dtype="uint8")), [1, 1, 1, 1, 1], [1, 0]], CSP) # All attributes passed, all attributes predicate
    bit_vector2 = AS.program_executor.filter(AS.aggregator.data_encrypted, [[1,0]], CSP, predicate_features=[2]) # All attributes passed, single attribute predicate
    bit_vector3 = AS.program_executor.filter(AS.program_executor.project(AS.aggregator.data_encrypted, 2), [[1,0]], CSP, predicate_features=[2], data_features=[2]) # Single attribute data, single attribute predicate

    decrypted_filter1 = CSP.decrypt_bit_vector(bit_vector1)
    decrypted_filter2 = CSP.decrypt_bit_vector(bit_vector2)
    decrypted_filter3 = CSP.decrypt_bit_vector(bit_vector3)

    if verbose:
        print("Full Data Test - Encoded Raw Data:", AS.aggregator.data_encoded)
        print("All attributes, All predicates Test:", decrypted_filter1)
        print("All attributes, Single Predicate Test:", decrypted_filter2)
        print("Single Attribute, Single Predicate Test:", decrypted_filter3)
        print("\n")

    assert decrypted_filter1 == [1,0,0,1,1]
    assert decrypted_filter2 == [1,0,0,1,1]
    assert decrypted_filter3 == [1,0,0,1,1]
    return True

def test_cross_product(verbose=True):
    result = AS.program_executor.cross_product(AS.aggregator.data_encrypted, 1, 2, CSP)
    result = [[[CSP.key_manager.private_key.lab_decrypt(value) for value in attribute]for attribute in row]for row in result]
    true_value = []
    for i in range(len(AS.aggregator.data_encoded)):
        true_value.append([])
        index = AS.aggregator.data_encoded[i][1].index(1)*len(AS.aggregator.data_encoded[i][2]) + AS.aggregator.data_encoded[i][2].index(1)
        length = len(AS.aggregator.data_encoded[i][1])*len(AS.aggregator.data_encoded[i][2])
        true_value[i].append(AS.aggregator.data_encoded[i][0])
        true_value[i].append([1 if i == index else 0 for i in range(length)])
    assert true_value == result
    return True
   
def test_group_by_count(verbose=True):
    result = AS.program_executor.group_by_count(AS.aggregator.data_encrypted, 2, CSP)
    result = [CSP.key_manager.private_key.lab_decrypt(value) for value in result]
    true_value = [3,2]

    if verbose:
        print("Query Result:", result)
        print("True Value:", true_value)

    assert result == true_value
    return True



# --- Basic encryption/encoding tests ---

# test_encrypt_decrypt()
# test_encode_decode()
# test_encrypted_data()

# --- Multiplication tests ---

# test_multiply_ciphers(CSP)
# test_HE_mult()

# --- Operator tests ---

# test_project()
# test_count()
# test_filter()
test_cross_product()
# test_group_by_count()