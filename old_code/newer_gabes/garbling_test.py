# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 13:44:17 2021

@author: Garret_H
"""
from cryptography.fernet import Fernet, InvalidToken
from Crypto.Random.random import shuffle
import pickle
from newer_gabes.label import Label

list1 = [Label(0),Label(1)]
list2 = [Label(0),Label(1)]

def garble(list1, list2):
        table = []
        check = []
        for label1 in list1:
            for label2 in list2:
                key1 = Fernet(label1.to_base64())
                key2 = Fernet(label2.to_base64())
                logic_value = label1.represents & label2.represents
                output_label = Label(1) if logic_value else Label(0)
                pickled = pickle.dumps(output_label)
                table_entry = key1.encrypt(key2.encrypt(pickled))
                table.append(table_entry)
        shuffle(table)
        return table

def ungarble(garblers_label, evaluators_label, table):
    for table_entry in table:
        try:
            key2 = Fernet(garblers_label.to_base64())
            key1 = Fernet(evaluators_label.to_base64())
            output_label = pickle.loads(key1.decrypt(key2.decrypt(table_entry)))
        except InvalidToken:
            # Wrong table entry, try again
            pass
    return output_label

garblers_label = list1[0]
evaluators_label = list2[1]

print("Garblers Label:", garblers_label)
print("Evaluators Label:", evaluators_label)

table = garble(list1, list2)
print("Table:", table)
print(ungarble(garblers_label, evaluators_label, table))