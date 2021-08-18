# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 10:37:40 2021

@author: Garret_H
"""

from pygarble.alice import Circuit
import json
import pickle
on_input_gates = [[0, "AND", [0, 1]], 
                [1, "XOR", [2, 3]], 
                [2, "OR", [0,3]]]

mid_gates = [[3, "XOR", [0, 1]],
             [4, "OR", [1, 2]],
             [5, 'NAND', [4, 4]]]
                

output_gates = [[6, "OR", [3, 4]]]
mycirc = Circuit(4, on_input_gates, mid_gates, output_gates)
my_input = [x[y] for x, y in zip(mycirc.poss_inputs, [0, 1, 0, 1])]
#mycirc.fire(my_input)
j = mycirc.prep_for_json()
print(type(j))
print(j)
with open('circuit.json','w') as file:
   json1.dump(j, file)