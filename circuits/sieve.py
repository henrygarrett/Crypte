# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 17:29:15 2021

@author: Garret_H
"""
#DONT TOUCH, IT WORKS
import json
from circuits.circuit import Circuit

class Sieve_circuit(Circuit):
    def __init__(self, number_of_elements, input_size):
        super().__init__(number_of_elements, input_size)
        
    def sieve(self):
        #RETURNS 0 IF NUMBER IS 0, 1 O/W
        for i in range(len(self.sieve_inputs)-1):
            if i%self.input_size == 0:
                start = max([self.circuit['gates'][-1]['id']] + self.circuit['alice'] + self.circuit['bob'])
                self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [self.sieve_inputs[i],self.sieve_inputs[i+1]]})
            elif i%self.input_size == self.input_size - 1:
                pass
            else:
                start = self.circuit['gates'][-1]['id']
                self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [start, self.sieve_inputs[i+1]]})
            if i%self.input_size == self.input_size - 2:
                self.adder1_inputs.append(self.circuit['gates'][-1]['id'])
        self.adder1_inputs = self.adder1_inputs[::-1]
        self.circuit['out'] = self.adder1_inputs
        with open('sieve.json','w') as file:
            json.dump(self.dictionary, file)
