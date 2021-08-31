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
        for i in range(self.number_of_elements):
            for j in range(1, self.input_size):
                if j == 1:
                    start = max(self.circuit['alice']) if i == 0 else self.circuit['gates'][-1]['id']
                    self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [i*self.input_size + self.input_size + 1,i*self.input_size + self.input_size + 2]})
                else:
                    start = self.circuit['gates'][-1]['id']
                    self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [start, i*self.input_size + self.input_size + j + 1]})
            self.adder1_inputs.append(self.circuit['gates'][-1]['id'])
                    
        self.circuit['out'] = self.adder1_inputs
        with open('sieve.json','w') as file:
            json.dump(self.dictionary, file)
