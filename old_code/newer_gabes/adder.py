# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 12:12:37 2021

@author: Garret_H
"""

circuit = {
  "name": "add",
  "circuits": [
    {
      "id": "1-bit full adder",
      "alice": [1, 2],
      "bob": [3],
      "out": [5, 11],
      "gates": [
        {"id": 4, "type": "XOR", "in": [2, 3]},
        {"id": 5, "type": "XOR", "in": [1, 4]},
        {"id": 6, "type": "AND", "in": [2, 3]},
        {"id": 7, "type": "AND", "in": [1, 4]},
        {"id": 11, "type": "OR", "in": [6, 7]}
      ]
    },
    {
      "id": "2-bit full adder",
      "alice": [1, 2, 12],
      "bob": [3, 13],
      "out": [5, 18, 15],
      "gates": [
        {"id": 4, "type": "XOR", "in": [2, 3]},
        {"id": 5, "type": "XOR", "in": [1, 4]},
        {"id": 6, "type": "AND", "in": [2, 3]},
        {"id": 7, "type": "AND", "in": [1, 4]},
        {"id": 11, "type": "OR", "in": [6, 7]},
        {"id": 14, "type": "XOR", "in": [12, 13]},
        {"id": 15, "type": "XOR", "in": [11, 14]},
        {"id": 16, "type": "AND", "in": [12, 13]},
        {"id": 17, "type": "AND", "in": [11, 14]},
        {"id": 18, "type": "OR", "in": [16, 17]}
      ]
    }
  ]
}