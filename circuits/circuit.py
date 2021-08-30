# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:02:52 2021

@author: Garret_H
"""
import copy
import math

class Circuit():
    def __init__(self, number_of_elements, input_size):
        self.number_of_elements = number_of_elements #ASSUMED GREATER THAN 1
        self.input_size = input_size #NUMBER OF BITS IN EACH NUMBER
        self.carry = 0
        self.adder1_inputs = []
        self.adder2_inputs = []
        self.sieve_inputs = []
        self.adder1_output_size = math.ceil(math.log(self.number_of_elements + 0.1, 2))# NUMBER OF BITS IN THE OUTPUT
        self.dictionary = {"name": "Test","circuits": [{"id": "counter","alice": None,"bob": None,"out": None,"gates": []}]}
        self.circuit = self.dictionary['circuits'][0]
        alice_length = self.input_size*self.number_of_elements +  self.adder1_output_size + 1
        self.circuit['alice'] = [i for i in range(alice_length)] # additional input gate so alice can add a zero input
        self.circuit['bob'] =   [i for i in range(alice_length, alice_length + self.input_size*self.number_of_elements)]
        
        self.inputs =  copy.deepcopy(self.circuit['alice'])
        self.inputs.extend(self.circuit['bob'])
        for n, value in enumerate(self.inputs):
            self.circuit['gates'].append({"id": -n-1, "type": "NOT", "in": [value]})
    
