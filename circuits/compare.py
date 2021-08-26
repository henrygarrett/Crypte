# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 19:20:47 2021

@author: Garret_H
"""

import difflib
import sys








a='''    def adder(self):
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

'''    
    
b='''    def adder(self):
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

'''



sys.stdout.writelines(difflib.unified_diff(a,b))