# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 12:51:24 2021

@author: Garret_H
"""

circuit = {
      "id": "Smart",
      "alice": [1, 2],
      "bob": [3, 4],
      "out": [7,8],
      "gates": [
        {"id": 5, "type": "AND", "in": [1, 3]},
        {"id": 6, "type": "XOR", "in": [2, 4]},
        {"id": 7, "type": "OR", "in": [5, 6]},
        {"id": 8, "type": "NOT", "in": [6]}
      ]
    }
  
