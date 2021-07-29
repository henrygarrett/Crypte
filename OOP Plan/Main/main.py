# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 09:51:30 2021

@author: madma
"""
import pathlib
import sys
import pickle
import os
import ast
PATH = str(pathlib.Path.cwd().parents[0])
sys.path.append(PATH + '\\CSP')
sys.path.append(PATH + '\\AS')
from CryptographicServiceProvider import CryptographicServiceProvider
import AnalyticsServer

AS = AnalyticsServer.AnalyticsServer()


if input('Replace budget, keys and data? y/n\n') != 'y':
    if 'budget.txt' not in os.listdir(PATH + '\\CSP'):
        print('There is no version so will create new budget, keys and data')
        CSP = CryptographicServiceProvider.CryptographicServiceProvider(input('What is the privacy budget?: '), True)
    
        #Creates Public and Private Keys and stores them in the appropriate places
        CSP.key_manager.generate_keys()
        
        public_key = CSP.key_manager.public_key
        
        #Creates then encodes then encrypts the data
        AS.aggregator.get_data()
        AS.aggregator.encode_data()
        AS.aggregator.encrypt_data(public_key)
    else:
        #Retrieves previous epsilon budget
        with open(PATH +'\\CSP\\budget.txt', 'r') as budget_file:
            CSP = CryptographicServiceProvider(int(budget_file.read()), True)
        
        #Retrieves previous public_key from save file    
        public_key = CSP.key_manager.public_key
        
        #Retrieves encrypted data and raw data
        with open(PATH + '\\Main\\data_set.txt', 'r') as data_file:
            AS.aggregator.data = ast.literal_eval(data_file.read())
    
        with open(PATH + '\\Main\\encrypted_data', 'rb') as data_file:
                AS.aggregator.data_encrypted = pickle.load(data_file) 
else:    
    CSP = CryptographicServiceProvider(input('What is the privacy budget?: '), True)
    
    #Creates Public and Private Keys and stores them in the appropriate places
    CSP.key_manager.generate_keys()
    
    public_key = CSP.key_manager.public_key
    
    #Creates then encodes then encrypts the data
    AS.aggregator.get_data()
    AS.aggregator.encode_data()
    AS.aggregator.encrypt_data(public_key)
    






# #Operators
new_data = AS.program_executor.group_by_count_encoded(public_key, AS.aggregator.data_encrypted, 1, CSP)
print(new_data)
                   