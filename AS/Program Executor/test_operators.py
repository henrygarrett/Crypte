# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 15:32:18 2021

@author: madma
"""
import sys
sys.path.append('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Lab Paillier')
import pickle
sys.path.append('C:\\Users\\madma\\Documents\\Internship\\Crypte\\AS\\Program Executor\\Operators')
import Operators
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\AS\\Aggregator\\aggregated_data','rb') as aggregated_data_file:
    data = pickle.load(aggregated_data_file)
with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Public_Key\\public_key','rb') as public_key_file:
    public_key = pickle.load(public_key_file)     
data2 = []
for i in range(10):
    data2.append([])
    for j in range(3):
        data2[i].append([])
        data2[i][j].append(j+1)

# new_data2 = Operators.filter_operator(public_key, data, [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1],[1,1]])
# print(new_data2)
new_data = Operators.group_by_count_encoded(public_key, data, 1)
print(new_data)
                        