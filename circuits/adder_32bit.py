# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 16:19:00 2021

@author: Garret_H
"""
import json
LENGTH = 32 # make even
dictionary = {"name": "Test","circuits":
              [{"id": "4-bit full subtractor",
                "alice": None,"bob": None,"out": None,"gates": []}]}
circuit = dictionary['circuits'][0]

circuit['alice'] = list(range(1, 2*LENGTH + 1, 2))[::-1]
circuit['bob'] = list(range(2, 2*LENGTH + 1, 2))[::-1]
print(circuit['alice'])

for value in circuit['alice'][::-1]:
    if value == 1:
        circuit['gates'].append({"id": 2*LENGTH + 1, "type": "XOR", "in": [1, 2]})
        circuit['gates'].append({"id": 2*LENGTH + 2, "type": "AND", "in": [1, 2]})
    else:
        start = 2*LENGTH + 2 + (value//2 - 1)*5
        circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [value, value + 1]})
        circuit['gates'].append({"id": start + 2, "type": "AND", "in": [value, value + 1]})
        circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [start,start + 1]})
        circuit['gates'].append({"id": start + 4, "type": "AND", "in": [start + 1, start]})
        circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
out = [2*LENGTH + 1]
out.extend([2*LENGTH + (value//2)*5 for value in circuit['alice'][::-1]])
print(out)
out.pop(1) # removes incorrect output index for first adder
print(out)
circuit['out'] = out
with open('adder_' + str(LENGTH) + 'bit.json','w') as file:
    json.dump(dictionary, file)
