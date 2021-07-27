# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:46:59 2021

@author: madma
"""
from pathlib import Path
path = str(Path.cwd().parents[1])
def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False
while True:
    budget = input('What is the privacy budget?: ')
    if check_float(budget):
        with open(path + '\\Crypte\\CSP\\Privacy Engine\\privacy_budget.txt',"w") as file:
            file.write(str(budget))
        break
    else:
        print('Please enter a real number as the value for the budget.ijrngdvf')