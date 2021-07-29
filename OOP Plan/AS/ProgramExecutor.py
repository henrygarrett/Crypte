import math
import random
import os
import pickle
import lab_paillier
path = 'C:\\Users\\madma\\Documents\\Internship'
class ProgramExecutor():
    def __init__(self):
        pass
    
    def cross_product(self, public_key, data_set, attribute1, attribute2):
        new_data_set = data_set
        for i, element in enumerate(new_data_set):
            vector1 = element.pop(attribute1)
            vector2 = element.pop(attribute2 if attribute1 > attribute2 else attribute2 - 1)
            vector_new = []
            for l in range(len(vector1)*len(vector2)):
                vector_new.append(public_key.general_lab_multiplication(vector1[math.floor(l/len(vector2))],vector2[l%len(vector2)]))
            element.append(vector_new)
        return new_data_set
    def project(self, data_set, attribute_chosen):
        new_data_set = []
        for element in data_set:
            new_data_set.append(element[attribute_chosen])
        return new_data_set
    def filter(self, public_key, data_set, predicate):#predicate inputed in double binary list i.e. [[0,1,0,1],[1,1,1,0],[1,1]]
        bit_vector = []    
        new_data_set = []
        for n, row in enumerate(data_set):
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
                        row_indicator = public_key.general_lab_multiplication(row_indicator,attribute_indicator)
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
                        product = public_key.general_lab_multiplication(row_indicator,data_set[n][i][j])
                        new_data_set[n][i].append(product)
            else:
                for j, value in enumerate(row):
                    product = public_key.general_lab_multiplication(row_indicator,data_set[n][j])
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
    def group_by_count(self, public_key, data_set, attribute):
        return_vector = []
        new_data_set = self.project(data_set, attribute)
        attribute_size =  len(data_set[0][attribute])
        for value in range(attribute_size):
            predicate = [[0  if i != value else 1 for i in range(attribute_size)]]
            blank, bit_vector = self.filter(public_key, new_data_set, predicate)
            return_vector.append(self.count(bit_vector))
        return return_vector
    
    def group_by_count_encoded(self, public_key, data_set, attribute):
        def rightRotate(lists, num):
            output_list = []
          
            # Will add values from n to the new list
            for item in range(len(lists) - num, len(lists)):
                output_list.append(lists[item])
              
            # Will add the values before
            # n to the end of new list    
            for item in range(0, len(lists) - num): 
                output_list.append(lists[item])
              
                return output_list
        gbc_vector = self.group_by_count(public_key, data_set, attribute)
        M = [random.randint(0,10**40) for n in range(len(gbc_vector))]
        gbc_vector_masked = [public_key.lab_encrypt(M[i], lab_paillier.gen_label(),lab_paillier.localGen(public_key)[0])._lab_add_encrypted(gbc_vector[i]) for i in range(len(gbc_vector))]
        with open(path + '\\Crypte\\CSP\\Data_Decryption\\Group_By_Count_Encoded\\gbc_vector_masked','wb') as gbc_vector_masked_file:
            pickle.dump(gbc_vector_masked, gbc_vector_masked_file)
        with open(path + '\\Crypte\\CSP\\Data_Decryption\\Group_By_Count_Encoded\\data_set_size.txt','w') as data_set_size_file:
            data_set_size_file.write(len(data_set))
        os.system(path + '\\Crypte\\CSP\\Data_Decryption\\Group_By_Count_Encoded\\group_by_count_encoded.py')
        with open(path + '\\Crypte\\AS\\Program Executor\\Operators\\gbce_return_vector_CSP', 'rb') as gbce_return_vector_file:
             return_vector_encrypted = pickle.load(gbce_return_vector_file)
        return [rightRotate(return_vector_encrypted[i],M[i]) for i in range(len(return_vector_encrypted))]
                        
                
            
        