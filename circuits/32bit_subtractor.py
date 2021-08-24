# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 16:19:00 2021

@author: Garret_H
"""
import json
length = 32 # make even
dictionary = {"name": "Test","circuits": [{"id": "4-bit full subtractor","alice": None,"bob": None,"out": None,"gates": []}]}
circuit = dictionary['circuits'][0]

circuit['alice'] = [i for i in range(1, 2*length + 1, 2)][::-1]
circuit['bob'] = [i for i in range(2, 2*length + 1, 2)][::-1]


for value in reversed(circuit['alice']):
    if value == 1:
        circuit['gates'].append({"id": 2*length + 1, "type": "XOR", "in": [1, 2]})
        circuit['gates'].append({"id": 2*length + 2, "type": "NOTAND", "in": [1, 2]})
    else:
        start = 2*length + 2 + (value//2 - 1)*5
        circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [value, value + 1]})
        circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [value, value + 1]})
        circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [start,start + 1]})
        circuit['gates'].append({"id": start + 4, "type": "NOTAND", "in": [start + 1, start]})
        circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
out = [2*length + 1]
out.extend([2*length + (value//2)*5 for value in reversed(circuit['alice'])])
out.pop(1) # removes incorrect output index for first adder
circuit['out'] = out
with open(str(length)+ 'bit_subtractor.json','w') as file:
    json.dump(dictionary, file)
