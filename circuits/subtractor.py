# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 16:19:00 2021

@author: Garret_H
"""




# for value in reversed(circuit['alice']):
#     if value == 1:
#         circuit['gates'].append({"id": 2*length + 1, "type": "XOR", "in": [1, 2]})
#         circuit['gates'].append({"id": 2*length + 2, "type": "NOTAND", "in": [1, 2]})
#     else:
#         start = 2*length + 2 + (value//2 - 1)*5
#         circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [value, value + 1]})
#         circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [value, value + 1]})
#         circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [start,start + 1]})
#         circuit['gates'].append({"id": start + 4, "type": "NOTAND", "in": [start + 1, start]})
#         circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
# out = [2*length + 1]
# out.extend([2*length + (value//2)*5 for value in reversed(circuit['alice'])])
# out.pop(1) # removes incorrect output index for first subtractor
# circuit['out'] = out
# with open(str(length)+ 'bit_subtractor.json','w') as file:
#     json.dump(dictionary, file)


import math
import json

class Subtractor_circuit():
    def __init__(self, number_of_elements):
        
        self.number_of_elements = number_of_elements #ASSUMED GREATER THAN 1
        self.sum_size = math.ceil(math.log(self.number_of_elements,2))# NUMBER OF BITS IN THE OUTPUT
        self.carry = 0
        
        self.dictionary = {"name": "Test","circuits": [{"id": "counter","alice": None,"bob": [-1],"out": None,"gates": []}]}
        self.circuit = self.dictionary['circuits'][0]
        
        self.circuit['alice'] = [i for i in range(self.number_of_elements + 1)] # additional input gate so alice can add a zero input
        self.circuit['gates'].append({"id": -2, "type": "OR", "in": [-1,0]}) #GATE FOR BOB TO APPEASE THE circuit GODS
        
        self.inputs = self.circuit['alice'][1:]

    def subtractor(self):
        difference= []
        for i in range(self.number_of_elements - 1):
            for j in range(self.sum_size):
                
                if j == 0:
                    if i == 0:
                        difference.append(self.half_subtractor(self.inputs[i], self.inputs[i+1]))
                    else:
                        difference.append(self.half_subtractor(difference.pop(0), self.inputs[i+1]))
                else:
                    if i == 0:
                        difference.append(self.full_subtractor(0, 0))
                    else:
                        difference.append(self.full_subtractor(difference.pop(0), 0))                     
        self.circuit['out'] = sum
        with open('counter.json','w') as file:
            json.dump(self.dictionary, file)    
    def half_subtractor(self, alice, bob):
        start = max(self.circuit['alice']) if len(self.circuit['gates']) == 1 else self.circuit['gates'][-1]['id']
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [alice, bob]})
        difference= start + 1
        self.carry = start + 2
        return difference       
    def full_subtractor(self, alice, bob):
        start = self.circuit['gates'][-1]['id']
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [self.carry, start + 1]})
        self.circuit['gates'].append({"id": start + 4, "type": "NOTAND", "in": [self.carry, start + 1]})
        self.circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
        difference= start + 3
        self.carry = start + 5
        return difference