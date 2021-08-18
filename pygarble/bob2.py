# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 11:03:40 2021

@author: Garret_H
"""

from pygarble.bob import Circuit
import json
with open('circuit.json', 'r') as file:
    json_data = json.load(file)
mycirc = Circuit(json_data)


with open('circuit.json') as data_file:    
    data = json.load(data_file)
    
mycirc = Circuit(data)