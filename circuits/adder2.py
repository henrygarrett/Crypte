# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:03:05 2021

@author: Garret_H
"""
import json
from circuits.circuit import Circuit
class Adder2(Circuit):
    '''
    used to define adder2 which adds mask to final count
    '''
    def adder2(self):
        '''
        second adder circuit for adding final mask to count
        '''
        total = []
        input2 = self.circuit['alice'][1 : self.adder1_output_size + 1][::-1]
        for j in range(self.adder1_output_size):
            if j == 0:
                total.append(self.half_adder(self.adder2_input.pop(0), input2[j]))
            else:
                total.append(self.full_adder(self.adder2_input.pop(0), input2[j]))

        self.circuit['out'] = total
        with open('adder2.json','w') as file:
            json.dump(self.dictionary, file)


    def half_adder(self, alice, bob):
        '''
        Half Adder Block
        '''
        start = [self.circuit['gates'][-1]['id']]
        start.extend(self.circuit['alice'])
        start.extend(self.circuit['bob'])
        start = max(start)
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "AND", "in": [alice, bob]})
        self.carry = start + 2
        return start + 1

    def full_adder(self, alice, bob):
        '''
        Full Adder block
        '''
        start = self.circuit['gates'][-1]['id']
        self.circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 2, "type": "AND", "in": [alice, bob]})
        self.circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [self.carry, start +1]})
        self.circuit['gates'].append({"id": start + 4, "type": "AND", "in": [self.carry, start +1]})
        self.circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
        self.carry = start + 5
        return start + 3
