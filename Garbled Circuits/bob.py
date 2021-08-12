# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:45:16 2021

@author: Garret_H
"""

> from pygarble.bob import *

with open('circuit.json', 'r') as file:
    json_data = json.loads(file)

mycirc = Circuit(json_data)