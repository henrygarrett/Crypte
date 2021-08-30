# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 19:20:47 2021

@author: Garret_H
"""

import difflib
import sys

with open('counter.py', 'r') as file:
    a = file.readlines()
    
with open('adder_w_fcts.py', 'r') as file:
    b = file.readlines()
    
    
sys.stdout.writelines(difflib.unified_diff(a,b))