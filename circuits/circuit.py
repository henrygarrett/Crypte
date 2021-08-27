# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:02:52 2021

@author: Garret_H
"""
import math
import json

class Circuit():
    def __init__(self, number_of_elements, input_size):
        self.number_of_elements = number_of_elements #ASSUMED GREATER THAN 1
        self.input_size = input_size #NUMBER OF BITS IN EACH NUMBER
        self.carry = 0
        self.adder1_inputs = []
        self.adder2_inputs = []
        self.filter_inputs = []
        self.adder1_output_size = math.ceil(math.log(self.number_of_elements+0.1,2))# NUMBER OF BITS IN THE OUTPUT
        print(self.adder1_output_size)
        
        self.dictionary = {"name": "Test","circuits": [{"id": "counter","alice": None,"bob": None,"out": None,"gates": []}]}
        self.circuit = self.dictionary['circuits'][0]
        
        
        self.circuit['alice'] = [i for i in range(self.input_size*self.number_of_elements +  self.adder1_output_size + 1)] # additional input gate so alice can add a zero input
        self.circuit['bob'] =   [i for i in range(self.input_size*self.number_of_elements + self.adder1_output_size + 1,(2*self.input_size*self.number_of_elements) +  self.adder1_output_size + 1)]
    def subtractor(self, lonely=False):
        if lonely:
            for i in range(0, self.input_size + 1):
                self.circuit['gates'].append({"id": 5000 + i, "type": "OR", "in": [i,i]})
        difference= []
        for i in range(self.number_of_elements * self.input_size):
            if i == 0:
                difference.append(self.half_subtractor(self.circuit['alice'][-i-1],self.circuit['bob'][-i-1]))
            else:
                difference.append(self.full_subtractor(self.circuit['alice'][-i-1],self.circuit['bob'][-i-1]))
        
        self.filter_inputs = difference
        self.circuit['out'] = difference
        with open('counter.json','w') as file:
            json.dump(self.dictionary, file)    

    def filter(self):
        #RETURNS 0 IF NUMBER IS 0, 1 O/W
        inputs = []
        for i in range(self.number_of_elements):
            for j in range(self.input_size - 1):
                start = self.circuit['gates'][-1]['id']
                if j == 0:
                    self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [self.filter_inputs[i*self.input_size + j], self.filter_inputs[i*self.input_size + j + 1]]})
                else:
                    self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [start, self.filter_inputs[i*self.input_size + j + 1]]})        
            inputs.append(self.circuit['gates'][-1]['id'])
        #GATES CORRESPONDING TO EACH NUMBERS INDICATOR BIT
        self.adder1_inputs = inputs
        self.circuit['out'] = self.adder1_inputs
        with open('counter.json','w') as file:
            json.dump(self.dictionary, file)

    def adder1(self):
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
        self.adder2_inputs = sum
        self.circuit['out'] = sum
        with open('counter.json','w') as file:
            json.dump(self.dictionary, file)    

    def adder2(self):
        sum= []
        print(self.adder2_inputs)
        for i, n in enumerate(self.adder2_inputs):
            if i == 0:
                sum.append(self.half_adder(n,self.circuit['alice'][i+1]))
            else:
               sum.append(self.full_adder(n,self.circuit['alice'][i+1]))
        
        self.circuit['out'] = sum
        with open('counter.json','w') as file:
            json.dump(self.dictionary, file)
            


            
    def half_adder(self, alice, bob):
        start = self.circuit['gates'][-1]['id']
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
    def half_subtractor(self, alice, bob):
        start = max(self.circuit['bob'])
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [alice, bob]})
        difference= start + 1
        self.carry = start + 2
        return difference       
    def full_subtractor(self, alice, bob):
        start = self.circuit['gates'][-1]['id']
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "NOTAND", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [start + 1, self.carry]})
        self.circuit['gates'].append({"id": start + 4, "type": "NOTAND", "in": [start + 1, self.carry]})
        self.circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
        difference= start + 3
        self.carry = start + 5
        return difference
    