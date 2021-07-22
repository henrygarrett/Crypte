# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 10:42:15 2021

@author: madma
"""

import sys
sys.path.append('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Lab Paillier')
import lab_paillier

import pickle
public_key, private_key = lab_paillier.generate_lab_paillier_keypair() 


with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\Public_Key\\public_key', 'wb') as public_key_file:
   pickle.dump(public_key, public_key_file)


with open('C:\\Users\\madma\\Documents\\Internship\\Crypte\\CSP\\Key Manager\\private_key', 'wb') as private_key_file:
   pickle.dump(private_key, private_key_file)


