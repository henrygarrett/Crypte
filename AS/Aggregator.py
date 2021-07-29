'''Gives several options for aggregating data, either:
import as a list.txt file, generate it randomly
or take input one at a time (as in real use case)'''
from pathlib import Path
import ast
import random
import pickle
import os
import sys
PATH= str(Path.cwd().parents[0])
sys.path.append(PATH + '\\Lab Paillier')




class Aggregator():
    '''the overall class for data aggregation.
    Contains three methods for aggregating data depending on input'''
    def __init__(self):
        self.data = self.get_data()
        self.data_encoded = None
        self.data_encrypted = None

    def get_data(self):
        if 'data_set.txt' in os.listdir(PATH + os.sep + 'AS'):
            with open('data_set.txt', 'r') as data_set_file:
                return ast.literal_eval(data_set_file.read())
        else:
            return self.set_data(5,True)
    def encode_data(self):
        if self.data is None:
            print('No data to encode!')
            return None
        data_encoded = []
        for value in self.data:
            countries = ['uk', 'france', 'germany', 'spain', 'italy']
            age_onehot_encoded = [0 for i in range(20,41)]
            age_onehot_encoded[int(value[0])-20] = 1#puts a 1 at the age-th position
            smoke_onehot_encoded = [1,0] if value[2] == 'yes' else [0,1]
            country_onehot_encoded = [0 for i in range(len(countries))]
            country_onehot_encoded[int(countries.index(value[1]))] = 1
            data_encoded.append([age_onehot_encoded,country_onehot_encoded,smoke_onehot_encoded])
        self.data_encoded = data_encoded
        return data_encoded
    def local_gen(self, public_key):
        seed = ''
        for _ in range(100):
            seed += str(random.randint(0,1))
        seed_encoded = int(seed,2)
        seed_encrypted = public_key.encrypt(seed_encoded, None)
        return bin(seed_encoded), seed_encrypted
    def gen_label(self):
        label = str(random.randint(1,9))
        for _ in range(29):
            label += str(random.randint(0,9))
        return int(label)
    def encrypt_data(self, public_key):
        if self.data_encoded is None:
            print('No encoded data to encrypt!')
            return None
        data_list = []
        for data in self.data_encoded:
            seed = self.local_gen(public_key)[0]
            label = self.gen_label()
            data_encrypted = [[public_key.lab_encrypt(value, label, seed)
                               for value in attribute] for attribute in data]
            data_list.append(data_encrypted)
        with open('encrypted_data', 'wb') as data_file:
            pickle.dump(data_list, data_file)
        self.data_encrypted = data_list
        return data_list

    def set_data(self, entries = 5, return_value = False):

        countries = ['uk', 'france', 'germany', 'spain', 'italy']
        data_set = []

        for _ in range(entries):
            age = str(random.randint(20,40))
            country = countries[random.randint(0,4)]
            smoke = 'yes' if random.randint(0,1) == 1 else 'no'
            data_set.append([age, country, smoke])
        with open('data_set.txt', 'w') as data_set_file:
            data_set_file.write(str(data_set))
        if return_value:
            return data_set
        return None



    def merge_encrypted_data(self, directory):
        merged_data = []
        #directory = PATH + '\\AS\\Raw Data'
        for filename in os.listdir(directory):
            with open(directory + '\\' + str(filename), 'rb') as data_file:
                merged_data.append(pickle.load(data_file))
        with open(PATH + '\\AS\\aggregated_data', 'wb') as aggregated_data_file:
            pickle.dump(merged_data, aggregated_data_file)
