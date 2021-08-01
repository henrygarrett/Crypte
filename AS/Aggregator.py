'''Gives several options for aggregating data, either:
import as a list.txt file, generate it randomly
or take input one at a time (as in real use case)'''
from pathlib import Path
import ast
import random
import pickle
import os
import sys
import numpy as np

class Aggregator():
    '''the overall class for data aggregation.
    Contains three methods for aggregating data depending on input'''
    def __init__(self):
        self.data = self.get_data()
        self.data_encoded = self.encode_data()
        self.data_encrypted = None

    def __str__(self):
        return "Raw Data - " + str(self.data)

    def get_data(self):
        if 'data_set.txt' in os.listdir(".." + os.sep + 'Main' + os.sep):
            with open('data_set.txt', 'r') as data_set_file:
                return ast.literal_eval(data_set_file.read())
        else:
            return self.set_data(5,True)

    # when we eventually use real data attribute map will contain a map of attributes to their list of values which will be used to one-hot encode
    def encode_data(self, attribute_map=None, attribute_nums=None):
        if self.data is None:
            print('No data to encode!')
            return None

        return [self.encode_row(row, attribute_map, attribute_nums) for row in self.data]

    # Maps a row of raw data to a one-hot encoded version, can optionally provide an attribute_map to with with other data than our toy dataset
    def encode_row(self, raw_row, attribute_map=None, attribute_nums=None):

        if attribute_map is None: # If this is None, then we are assuming our toy dataset with 3 attributes
            countries = ['uk', 'france', 'germany', 'spain', 'italy']
            smoker = ["yes", "no"]
            ages = [str(i) for i in range(20,41)]
            attribute_map = {"ages": ages, "countries": countries, "smoker": smoker}

        if attribute_nums is None: # If the attribute_nums is None, then we assume we are being provided a dataset with all attributes and will map all of them
            attribute_nums = range(0,len(attribute_map.keys()))

        encoded_row = []
        for i, val in enumerate(raw_row):
            attr_num = attribute_nums[i]
            attr_map = list(attribute_map.values())[attr_num]
            one_hot_index = attr_map.index(val)
            one_hot = np.zeros(len(attr_map), dtype="uint8")
            one_hot[one_hot_index] = 1
            encoded_row.append(list(one_hot))

        return encoded_row

    def decode_data(self, encoded_data, attribute_map=None, attribute_nums=None):
        return [self.decode_row(encoded_row, attribute_map, attribute_nums) for encoded_row in encoded_data]

    # decodes a row of raw data
    def decode_row(self, encoded_row, attribute_map=None, attribute_nums=None):
        decoded_data = []

        if attribute_map is None: # If this is None, then we are assuming our toy dataset with 3 attributes
            countries = ['uk', 'france', 'germany', 'spain', 'italy']
            smoker = ["yes", "no"]
            ages = [i for i in range(20,41)]
            attribute_map = {"ages": ages, "countries": countries, "smoker": smoker}

        if attribute_nums is None: # If the attribute_nums is None, then we assume we are being provided a dataset with all attributes and will map all of them
            attribute_nums = range(0,len(attribute_map.keys()))

        for i,attr_num in enumerate(attribute_nums):
            decoded_data.append(list(attribute_map.values())[attr_num][encoded_row[i].index(1)])

        return decoded_data

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