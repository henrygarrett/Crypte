# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:03:05 2021

@author: Garret_H
"""
import json
from circuits.circuit import Circuit
class Adder1(Circuit):
    def __init__(self,number_of_elements, input_size):
        super().__init__(number_of_elements, input_size)
        
        
    
    
    
    def adder1(self):
        total = []
        self.adder1_input = self.circuit['bob'][:self.number_of_elements]
        for i in range(self.number_of_elements - 1):
            for j in range(self.adder1_output_size):
                if j == 0:
                    if i == 0:
                        total.append(self.half_adder(self.adder1_input.pop(0), self.adder1_input.pop(0)))
                    else:
                        total.append(self.half_adder(total.pop(0), self.adder1_input.pop(0)))
                else:
                    if i == 0:
                        total.append(self.full_adder(0, 0))
                    else:
                        total.append(self.full_adder(total.pop(0), 0))
        self.adder2_input = total
        self.circuit['out'] = total
        with open('adder1.json','w') as file:
            json.dump(self.dictionary, file)
    

    def half_adder(self, alice, bob):
        start = max(max(self.circuit['alice']),max(self.circuit['bob']), max([x['id'] for x in self.circuit['gates']]))
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "AND", "in": [alice, bob]})
        self.carry = start + 2
        return start + 1        
    
    def full_adder(self, alice, bob):
        start = self.circuit['gates'][-1]['id']
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "AND", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [self.carry, start + 1]})
        self.circuit['gates'].append({"id": start + 4, "type": "AND", "in": [self.carry, start + 1]})
        self.circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
        self.carry = start + 5
        return start + 3