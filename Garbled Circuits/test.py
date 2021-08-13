# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 11:11:20 2021

@author: Garret_H
"""
from cryptography.hazmat.primitives.asymmetric import rsa
from random import randint
import pickle
from cryptography.hazmat.backends import default_backend
from new_gabes.label import Label
from new_gabes.network import send_data, receive_data


m0 = Label(0)
m1 = Label(1)


private_key = rsa.generate_private_key(public_exponent=65537,key_size=512,backend=default_backend())
d = private_key.private_numbers().d
public_key = private_key.public_key()
m, f = public_key.public_numbers().n, public_key.public_numbers().e
y0, y1 = [randint(2, m // 2) for _ in range(2)]


send_data('list1',[y0, y1, m, f])
x0, x1, n, e = receive_data('list1')


k = randint(2, n // 2)
b = 1
chosen_x = x1 if b == '1' else x0
w = (chosen_x + pow(k, e, n)) % n


send_data('w',w)
v = receive_data('w')


k0, k1 = [pow((v - x), d, n) for x in (x0, x1)]
bytes_m0 = pickle.dumps(m0)
bytes_m1 = pickle.dumps(m1)
m0 = int.from_bytes(bytes_m0, byteorder='big')
m1 = int.from_bytes(bytes_m1, byteorder='big')


send_data('list2',[m0 + k0, m1 + k1, len(bytes_m0), len(bytes_m1)])
t0, t1, size_m0, size_m1 = receive_data('list2')


chosen_t = t1 if b == '1' else t0
chosen_size = size_m1 if b == '1' else size_m0
m = chosen_t - k
label = pickle.loads(int.to_bytes(m, length=chosen_size, byteorder='big'))
print(type(label))







