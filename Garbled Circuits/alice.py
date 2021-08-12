# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:35:56 2021

@author: Garret_H
"""
from pygarble.ot import *
from pygarble.alice import keypair # we will use this to generate some example keys

from pygarble.alice import *
import json
import pygarble.json_stuff
on_input_gates = [[0, "AND", [0, 1]], 
                [1, "XOR", [2, 3]], 
                [2, "OR", [0,3]]]
mid_gates = [[3, "XOR", [0, 1]],
             [4, "OR", [1, 2]]]
output_gates = [[5, "OR", [3, 4]]]
mycirc = Circuit(4, on_input_gates, mid_gates, output_gates)
my_input = [x[y] for x, y in zip(mycirc.poss_inputs, [0, 1, 0, 1])]
print(my_input)
print(mycirc.fire(my_input))

j = mycirc.prep_for_json()

write_json(file, j)



my_keypair = list(keypair().values())
my_keypair
[b'tWiWGameWDMNOTUDRBM2FUWHkpPg9ZqWPM_e3bsvdqc=', b'5-x4_N0gwM_Hh0AYnSykYn2Ab4sCUw9iUzBVw9ZK8tw=']
alice = Alice(my_keypair)