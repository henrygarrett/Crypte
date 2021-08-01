import math
import random
import os
import pickle

path = 'C:\\Users\\madma\\Documents\\Internship'

class ProgramExecutor():
    def __init__(self, encrypted_data=None):
        self.encrypted_data = encrypted_data
    
    def cross_product(self, public_key, attribute1, attribute2, CSP):
        new_data_set = self.encrypted_data
        for i, element in enumerate(new_data_set):
            vector1 = element.pop(attribute1)
            vector2 = element.pop(attribute2 if attribute1 > attribute2 else attribute2 - 1)
            vector_new = []
            for l in range(len(vector1)*len(vector2)):
                vector_new.append(public_key.general_lab_multiplication(vector1[math.floor(l/len(vector2))],vector2[l%len(vector2)]), CSP)
            element.append(vector_new)
        return new_data_set

    def project(self, attribute_chosen, CSP):
        new_data_set = []
        for element in self.encrypted_data:
            new_data_set.append(element[attribute_chosen])
        return new_data_set

    def filter(self, public_key, predicate, CSP):#predicate inputed in double binary list i.e. [[0,1,0,1],[1,1,1,0],[1,1]]
        bit_vector = []    
        new_data_set = []
        for n, row in enumerate(self.encrypted_data):
            new_data_set.append([])
            for i, attribute in enumerate(row):
                if len(predicate) != 1:
                    for j, condition in enumerate(predicate[i]):
                        if condition == 1:
                            try:
                                attribute_indicator = attribute[j]._lab_add_encrypted(attribute_indicator)
                            except UnboundLocalError:
                                attribute_indicator = attribute[j]
                    try:
                        row_indicator = public_key.general_lab_multiplication(row_indicator,attribute_indicator, CSP)
                    except UnboundLocalError:
                        row_indicator = attribute_indicator
                else:
                    for j, condition in enumerate(predicate[0]):
                        if condition == 1:
                            try:
                                attribute_indicator = attribute._lab_add_encrypted(attribute_indicator)
                            except UnboundLocalError:
                                attribute_indicator = attribute
                    row_indicator = attribute_indicator
            if len(predicate) != 1:
                for i, attribute in enumerate(row):
                    new_data_set[n].append([])
                    for j, value in enumerate(attribute):
                        product = public_key.general_lab_multiplication(row_indicator,self.encrypted_data[n][i][j], CSP)
                        new_data_set[n][i].append(product)
            else:
                for j, value in enumerate(row):
                    product = public_key.general_lab_multiplication(row_indicator,self.encrypted_data[n][j], CSP)
                    new_data_set[n].append(product)
            bit_vector.append(row_indicator)
                
        return new_data_set, bit_vector
    
    def count(self, bit_vector):
        for i, value in enumerate(bit_vector):
            try:
                total = value._lab_add_encrypted(total)
            except UnboundLocalError:
                total = value
        return total

    def group_by_count(self, public_key, attribute, CSP):
        return_vector = []
        new_data_set = self.project(self.encrypted_data, attribute, CSP)
        attribute_size =  len(self.encrypted_data[0][attribute])
        for value in range(attribute_size):
            predicate = [[0  if i != value else 1 for i in range(attribute_size)]]
            blank, bit_vector = self.filter(public_key, new_data_set, predicate, CSP)
            return_vector.append(self.count(bit_vector))
        return return_vector
    
    def group_by_count_encoded(self, public_key, attribute, CSP):
        def rightRotate(lists, num):
            output_list = []
            print(list)
            # Will add values from n to the new list
            for item in range(len(lists) - (num%len(lists)), len(lists)):
                output_list.append(lists[item])
              
            # Will add the values before
            # n to the end of new list    
            for item in range(0, len(lists) - num): 
                output_list.append(lists[item])

            return output_list
        gbc_vector = self.group_by_count(public_key, self.encrypted_data, attribute, CSP)
        M = [random.randint(0,10**5) for n in range(len(gbc_vector))]
        gbc_vector_masked = [public_key.lab_encrypt(M[i], self.gen_label(),self.local_gen(public_key)[0])._lab_add_encrypted(gbc_vector[i]) for i in range(len(gbc_vector))]
        return_vector_encrypted = CSP.group_by_count_encoded(gbc_vector_masked, len(self.encrypted_data))
        return [rightRotate(return_vector_encrypted[i], M[i]) for i in range(len(return_vector_encrypted))]
                        
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
        