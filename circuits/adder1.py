# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:02:52 2021

@author: Garret_H
"""
import json
from circuits.circuit import Circuit

class Adder1_circuit(Circuit):
    def __init__(self, number_of_elements, input_size):
        super().__init__(number_of_elements, input_size)


    def adder1(self):
        if self.adder1_inputs == []:
            self.adder1_inputs = [self.circuit['bob'][i] for i in range(0,self.input_size*self.number_of_elements,self.input_size)]
        sum = []
        for i in range(self.number_of_elements - 1):
            for j in range(self.adder1_output_size):
                if j == 0:
                    if i == 0:
                        sum.append(self.half_adder(self.adder1_inputs[i], self.adder1_inputs[i+1]))
                    else:
                        sum.append(self.half_adder(sum.pop(0), self.adder1_inputs[i+1]))
                else:
                    if i == 0:
                        sum.append(self.full_adder(0, 0))
                    else:
                        sum.append(self.full_adder(sum.pop(0), 0))                     
        self.circuit['out'] = sum
        with open('adder1.json','w') as file:
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
