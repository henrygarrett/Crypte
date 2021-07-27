# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 10:42:15 2021

@author: madma
"""
from pathlib import Path
path = str(Path.cwd().parents[2])
import sys
sys.path.append(path + '\\Crypte\\Lab Paillier')
import lab_paillier

import pickle
public_key, private_key = lab_paillier.generate_lab_paillier_keypair() 


with open(path + '\\Crypte\\Public_Key\\public_key', 'wb') as public_key_file:
   pickle.dump(public_key, public_key_file)


with open(path + '\\Crypte\\CSP\\Key Manager\\private_key', 'wb') as private_key_file:
   pickle.dump(private_key, private_key_file)


