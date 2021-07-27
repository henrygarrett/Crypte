from pathlib import Path
path = str(Path.cwd().parents[2])
import sys
sys.path.append(path + '\\Crypte\\Lab Paillier')
import pickle
import os
sys.path.append(path + '\\Crypte\\AS\\Program Executor\\Operators')
import ast
import random

class Aggregator():
    def __init__(self):
        self.data_set = self.get_data()

    def get_data(self):
        with open('data_set.txt', 'w') as data_set_file:
            data_set = ast.literal_eval(data_set_file.read())
        return data_set

       
    def set_data(self,entries, return_value):
        
        countries = ['uk', 'france', 'germany', 'spain', 'italy']
        data_set = []

        for i in range(entries):
            age = str(random.randint(20,40))
            country = countries[random.randint(0,4)]
            smoke = 'yes' if random.randint(0,1) == 1 else 'no'
            data_set.append([age, country, smoke])
        with open('data_set.txt', 'w') as data_set_file:
            data_set_file.write(str(data_set))
        if return_value:
            return data_set


    def merge_encrypted_data(directory):
        merged_data = []
        #directory = path + '\\Crypte\\AS\\Aggregator\\Raw Data'
        for filename in os.listdir(directory):
            with open(directory + '\\' + str(filename), 'rb') as data_file:
                merged_data.append(pickle.load(data_file))   
        with open(path + '\\Crypte\\AS\\Aggregator\\aggregated_data','wb') as aggregated_data_file:
            pickle.dump(merged_data, aggregated_data_file)