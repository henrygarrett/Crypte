# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 17:29:15 2021

@author: Garret_H
"""
import math
import json

class Circuit():
    def __init__(self, number_of_elements, size):
        self.size = size #NUMBER OF BITS IN EACH NUMBER
        
        
        self.number_of_elements = number_of_elements #ASSUMED GREATER THAN 1
        self.sum_size = math.ceil(math.log(self.number_of_elements + 0.1,2))# NUMBER OF BITS IN THE OUTPUT
    
    
        
        
        
        
        
        self.dictionary = {"name": "Test","circuits": [{"id": "counter","alice": None,"bob": [-1],"out": None,"gates": []}]}
        self.circuit = self.dictionary['circuits'][0]
        
        
        self.circuit['alice'] = [i for i in range(self.size*self.number_of_elements + 1)] # additional input gate so alice can add a zero input
        
        
        
        self.carry = 0
        
        #self.circuit['alice'] = [i for i in range(self.number_of_elements + 1)] # additional input gate so alice can add a zero input
        self.circuit['gates'].append({"id": -2, "type": "OR", "in": [-1,-1]}) #GATE FOR BOB TO APPEASE THE circuit GODS
        self.inputs = None
        
        
        
        
        

        
        
    def counter(self):
        #RETURNS 0 IF NUMBER IS 0, 1 O/W
        for i in range(self.number_of_elements):
            for j in range(1, self.size):
                if j == 1:
                    start = max(self.circuit['alice']) if i == 0 else self.circuit['gates'][-1]['id']
                    self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [i*self.size + 1,i*self.size + 2]})
                else:
                    start = self.circuit['gates'][-1]['id']
                    self.circuit['gates'].append({"id": start + 1, "type": "OR", "in": [start, i*self.size + j + 1]})        
                    
        #GATES CORRESPONDING TO EACH NUMBERS INDICATOR BIT
        inputs = [self.size*self.number_of_elements + i*(self.size-1) for i in range(1, self.number_of_elements + 1)]
        # self.circuit['out'] = inputs
        # with open('counter.json','w') as file:
        #     json.dump(self.dictionary, file)
        self.inputs = inputs
       
    
    
    def adder(self):
        sum = []
        for i in range(self.number_of_elements - 1):
            for j in range(self.sum_size):
                
                if j == 0:
                    if i == 0:
                        sum.append(self.half_adder(self.inputs[i], self.inputs[i+1]))
                    else:
                        sum.append(self.half_adder(sum.pop(0), self.inputs[i+1]))
                else:
                    if i == 0:
                        sum.append(self.full_adder(0, 0))
                    else:
                        sum.append(self.full_adder(sum.pop(0), 0))                     
        self.circuit['out'] = sum
        with open('counter.json','w') as file:
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
        

    
    
    
    
    
        
    