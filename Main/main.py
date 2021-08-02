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
    AS = AnalyticsServer()

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

    public_key = CSP.key_manager.public_key  # Obtain public key

    if generate_keys:
        # Creates then encodes then encrypts the data
        AS.aggregator.get_data()
        AS.aggregator.encode_data()
        AS.aggregator.encrypt_data(public_key)
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
AS.init_executor() # Once encrypted data is calculated/aggregated we update the ProgramExecutor instance to store a copy of the encrypted data to work on

# Raw data for the tests
TEST_DATA = [['25', 'spain', 'yes'], ['38', 'france', 'no'], ['39', 'italy', 'no'], ['29', 'italy', 'yes'], ['22', 'italy', 'yes']]

# Test functions

# Tests that the aggregator correctly encodes and decodes data to and from one-hot vector form
def test_encode_decode(verbose=True):
    encoded_data = AS.aggregator.data_encoded[0]
    decoded_data = AS.aggregator.decode_row(AS.aggregator.data_encoded[0])
    decoded_data = [str(val) for val in decoded_data]
    raw_data = [str(val) for val in AS.aggregator.data[0]]

    if verbose:
        print("Decoded Data:" + str(decoded_data))
        print("Raw Data:" + str(raw_data))
        print("Test Result:", str(decoded_data == raw_data))
        print("\n")

    assert decoded_data == raw_data

# Tests the Project Operator works correctly
def test_project(verbose=True):

    # Compute test query
    query_result = CSP.decrypt_data(AS.program_executor.project([0,2]))
    query_result = AS.aggregator.decode_data(query_result, attribute_nums=[0,2])
    query_result = list(map(lambda x: [str(val) for val in x], query_result)) # Raw data are strings

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

# Tests the Filter operator works correctly
def test_filter():
    new_data, bit_vector = AS.program_executor.filter(CSP.key_manager.public_key, [[1,1,1,1],[1,1,1,1],[1,0]], CSP)
    print(new_data)

# test_encode_decode()
test_project()
# test_filter()

