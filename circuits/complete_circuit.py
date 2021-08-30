# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:02:52 2021

@author: Garret_H
"""
from circuits.subtractor import Subtractor_circuit
from circuits.adder1 import Adder1_circuit
from circuits.adder2 import Adder2_circuit
from circuits.sieve import Sieve_circuit

class Complete_circuit(Subtractor_circuit, Adder1_circuit, Adder2_circuit, Sieve_circuit):
    def __init__(self, number_of_elements, input_size):
        super().__init__(number_of_elements, input_size)
    
    def subtractor():
        super().subtractor()

    def sieve(self):
        super().sieve()

    def adder1(self):
        super().adder1()
        
    def adder2(self):
        super.adder2()
            

