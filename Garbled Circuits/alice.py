# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:35:56 2021

@author: Garret_H
"""
from pygarble.ot import *
from pygarble.alice import keypair # we will use this to generate some example keys

from pygarble.alice import *
import json

def custom_to_json(python_object): # for dealing with bytes, borrowed from www.diveintopython3.net/serializing.html
    if isinstance(python_object, bytes):
        return {"__class__": "bytes", "__value__": list(python_object)}
    else:
        raise TypeError(repr(python_object) + " not JSON serializable or not bytes.")

def write_json(file_name, j):
    with open(file_name, 'w') as outfile:
        json.dump(j, outfile, default=custom_to_json, separators=(',', ':'))

def read_json(file_name):
    with open(file_name) as data_file:
        j = json.load(data_file)
    return j


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

write_json("circuit.json", j)

my_keypair = list(keypair().values())
alice = Alice(my_keypair)