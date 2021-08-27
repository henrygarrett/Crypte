# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 17:29:15 2021

@author: Garret_H
"""
import json
from circuits.adder import Adder_circuit

class Counter_circuit(Adder_circuit):
    def __init__(self, number_of_elements, input_size):
        Adder_circuit.__init__(self, number_of_elements)

        self.input_size = input_size #NUMBER OF BITS IN EACH NUMBER
        
        self.circuit['alice'] = [i for i in range(self.input_size*self.number_of_elements + 1)] # additional input gate so alice can add a zero input
        
        self.inputs = None
        
    def counter(self):
        #RETURNS 0 IF NUMBER IS 0, 1 O/W
        for i in range(self.number_of_elements):
            for j in range(1, self.input_size):
                if j == 1:
                    start = max(self.circuit['alice']) if i == 0 else self.circuit['gates'][-1]['id']
                    self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [i*self.input_size + 1,i*self.input_size + 2]})
                else:
                    start = self.circuit['gates'][-1]['id']
                    self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [start, i*self.input_size + j + 1]})        
                    
        #GATES CORRESPONDING TO EACH NUMBERS INDICATOR BIT
        self.inputs = [self.input_size*self.number_of_elements + i*(self.input_size-1) for i in range(1, self.number_of_elements + 1)]
        self.circuit['out'] = self.inputs
        with open('counter.json','w') as file:
            json.dump(self.dictionary, file)
