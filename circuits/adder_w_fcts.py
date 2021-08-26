# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:02:52 2021

@author: Garret_H
"""



import json
LENGTH = 8 # make even
dictionary = {"name": "Test","circuits":
              [{"id": "4-bit full subtractor",
                "alice": None,"bob": None,"out": None,"gates": []}]}
circuit = dictionary['circuits'][0]

circuit['alice'] = list(range(2*LENGTH -1, 0, -2))
circuit['bob'] = list(range(2*LENGTH, 0, -2))




def half_adder():
    circuit['gates'].append({"id": 2*LENGTH + 1, "type": "XOR", "in": [1, 2]})
    circuit['gates'].append({"id": 2*LENGTH + 2, "type": "AND", "in": [1, 2]})
    return 2*LENGTH + 1

def full_adder(value):
    start = 2*LENGTH + 2 + (value//2 - 1)*5
    circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [value, value + 1]})
    circuit['gates'].append({"id": start + 2, "type": "AND", "in": [value, value + 1]})
    circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [start, start + 1]})
    circuit['gates'].append({"id": start + 4, "type": "AND", "in": [start, start + 1]})
    circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
    return start + 3

out = [half_adder()]
out.append(full_adder(3))
out.append(full_adder(5))
out.append(full_adder(7))
circuit['out'] = out

print(circuit)
with open('adder_' + str(LENGTH) + 'bit.json','w') as file:
    json.dump(dictionary, file)
