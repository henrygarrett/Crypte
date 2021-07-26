# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 12:08:50 2021

@author: madma
"""
import random
countries = ['uk', 'france', 'germany', 'spain', 'italy']
data_set = []

for i in range(5):
    smoke = 'yes' if random.randint(0,1) == 1 else 'no'
    age = str(random.randint(20,40))
    country = countries[random.randint(0,4)]
    data_set.append([age, country, smoke])

with open('data_set.txt', 'w') as data_set_file:
    data_set_file.write(str(data_set))
    