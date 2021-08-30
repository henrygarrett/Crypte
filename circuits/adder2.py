# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:02:52 2021

@author: Garret_H
"""
import json
from circuits.circuit import Circuit

class Adder2_circuit(Circuit):
    def __init__(self, number_of_elements):
        super.__init__(number_of_elements)

    def adder2(self):
        total= []
        print(self.adder2_inputs)
        for i, n in enumerate(self.adder2_inputs):
            if i == 0:
                total.append(self.half_adder(n,self.circuit['alice'][i+1]))
            else:
               total.append(self.full_adder(n,self.circuit['alice'][i+1]))
        
        self.circuit['out'] = total
        with open('adder2.json','w') as file:
            json.dump(self.dictionary, file)
  
    def half_adder(self, alice, bob):
        start = max(self.circuit['alice']) if len(self.circuit['gates']) == 1 else self.circuit['gates'][-1]['id']
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "AND", "in": [alice, bob]})
        sum = start + 1
        self.carry = start + 2
        return sum        
    def full_adder(self, alice, bob):
        start = self.circuit['gates'][-1]['id']
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "AND", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [self.carry, start + 1]})
        self.circuit['gates'].append({"id": start + 4, "type": "AND", "in": [self.carry, start + 1]})
        self.circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
        sum = start + 3
        self.carry = start + 5
        return sum