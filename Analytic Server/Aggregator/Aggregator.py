# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 11:37:50 2021

@author: madma
"""
import sys
sys.path.append('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Lab Paillier')
import pickle
import os
sys.path.append('C:\\Users\\madma\\Documents\\Internship\\Crypte\\AS\\Program Executor\\Operators')
import Operators

aggregated_data = []
directory = 'C:\\Users\\madma\\Documents\\Internship\\Crypte\\AS\\Aggregator\\Raw Data'
for filename in os.listdir(directory):
    with open(directory + '\\' + str(filename), 'rb') as data_file:
        aggregated_data.append(pickle.load(data_file))   
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\AS\\Aggregator\\aggregated_data','wb') as aggregated_data_file:
    pickle.dump(aggregated_data, aggregated_data_file)