 # -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 16:19:00 2021

@author: Garret_H
"""
#DONT TOUCH, IT WORKS
import json
from circuits.circuit import Circuit

class Subtractor_circuit(Circuit):
    def __init__(self, number_of_elements, input_size):
        super().__init__(number_of_elements, input_size)
        
    def subtractor(self):
        difference= []
        for i in range(self.number_of_elements * self.input_size):
            if i == 0:
                difference.append(self.half_subtractor(self.circuit['alice'][-i-1],self.circuit['bob'][-i-1]))
            else:
                difference.append(self.full_subtractor(self.circuit['alice'][-i-1],self.circuit['bob'][-i-1]))
        self.sieve_inputs = difference
        self.circuit['out'] = difference
        with open('subtractor.json','w') as file:
            json.dump(self.dictionary, file)
        
    def half_subtractor(self, alice, bob):
        start = max(self.circuit['bob'])
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [alice, bob]})
        self.carry = start + 2
        return start + 1      
    def full_subtractor(self, alice, bob):
        start = self.circuit['gates'][-1]['id']
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [start + 1, self.carry]})
        self.circuit['gates'].append({"id": start + 4, "type": "NOTAND", "in": [start + 1, self.carry]})
        self.circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
        self.carry = start + 5
        return start + 3
    