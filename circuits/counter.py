# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 17:29:15 2021

@author: Garret_H
"""
import math
number_of_elements = 5 # assumed greater than 1
count_size = math.ceil(math.log(number_of_elements,2))
size = 32
import json
dictionary = {"name": "Test","circuits": [{"id": "Counter","alice": None,"bob": [999999999999],"out": None,"gates": []}]}
circuit = dictionary['circuits'][0]

circuit['alice'] = [i for i in range(size*number_of_elements + 1)]
circuit['alice'].append(5000)# additional input gate so alice can add a zero input


for i in range(number_of_elements):
    start = size*number_of_elements + i*(size-1) - 1
    for j in range(1, size):
        if j == 1:
            circuit['gates'].append({"id": start + 1, "type": "OR", "in": [i*size,i*size + 1]})
        else:
            circuit['gates'].append({"id": start + j, "type": "OR", "in": [start + j - 1, i*size + j]})
    

starter = number_of_elements*(size-1) + size*number_of_elements

inputs = [size*number_of_elements + i*(size-1) - 1 for i in range(1, number_of_elements + 1)]

oldstart =[]

# for i in range(number_of_elements - 1):
#     for j in range(count_size):
#         start = starter + i*((count_size-1)*5 + 2)
#         if i == 0:
#             if j == 0:
#                 circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [inputs[0], inputs[1]]})
#                 circuit['gates'].append({"id": start + 2, "type": "AND", "in": [inputs[0], inputs[1]]})
#                 old_start = start
#             else:
#                 start = start + 2 + (j-1)*5
#                 circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [5000,5000]})
#                 circuit['gates'].append({"id": start + 2, "type": "AND", "in": [5000,5000]})
#                 circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [start,start + 1]})
#                 circuit['gates'].append({"id": start + 4, "type": "AND", "in": [start + 1, start]})
#                 circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
#                 oldstart.append(start)
#         else:
#             if j == 0:
#                 circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [old_start + 1, inputs[i+1]]})
#                 circuit['gates'].append({"id": start + 2, "type": "AND", "in": [old_start + 1, inputs[i+1]]})
#                 old_start = start
#             else:
#                 start = start + 2 + (j-1)*5
#                 circuit['gates'].append({"id": start + 1, "type": "XOR", "in": [oldstart[0] + 5, 5000]})
#                 circuit['gates'].append({"id": start + 2, "type": "AND", "in": [oldstart.pop(0) + 5, 5000]})
#                 circuit['gates'].append({"id": start + 3, "type": "XOR", "in": [start,start + 1]})
#                 circuit['gates'].append({"id": start + 4, "type": "AND", "in": [start + 1, start]})
#                 circuit['gates'].append({"id": start + 5, "type": "OR", "in": [start + 2, start + 4]})
#                 oldstart.append(start)
    
    
# count = [start + i + 3 for i in range(0, -5*(count_size - 2) - 1, -5)]
# count.append(start-5*(count_size - 2)-1)
# print(count)
circuit['out'] = inputs

with open('counter.json','w') as file:
    json.dump(dictionary, file)
