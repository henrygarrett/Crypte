# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 13:02:52 2021

@author: Garret_H
"""
from circuits.subtractor import Subtractor_circuit
from circuits.adder1_circuit import Adder1
from circuits.adder2_circuit import Adder2
from circuits.sieve import Sieve_circuit

class Complete_circuit(Subtractor_circuit, Adder1, Adder2, Sieve_circuit):
    def __init__(self, number_of_elements, input_size):
        super().__init__(number_of_elements, input_size)
    
    def subtractor(self):
        super().subtractor()

    def sieve(self):
        super().sieve()

    def adder1(self):
        super().adder1()
        
    def adder2(self):
        super.adder2()
            

