import math
import random
import numpy as np

class ProgramExecutor():
    def __init__(self, public_key, num_rows, num_attr):
        self.public_key = public_key
        self.num_rows = num_rows # Number of rows in the dataset
        self.num_attr = num_attr # Number of attributes in the dataset
        # Both of the above are needed for filtering
    
    def cross_product(self, encrypted_data, attribute1, attribute2, CSP):
        new_data_set = encrypted_data
        for i, element in enumerate(new_data_set):
            vector1 = element.pop(attribute1)
            vector2 = element.pop(attribute2 if attribute1 > attribute2 else attribute2 - 1)
            vector_new = []
            for l in range(len(vector1)*len(vector2)):
                vector_new.append(self.public_key.general_lab_multiplication(vector1[math.floor(l/len(vector2))],vector2[l%len(vector2)]), CSP)
            element.append(vector_new)
        return new_data_set

    def project(self, encrypted_data, attributes_chosen):
        new_data_set = []
        for element in encrypted_data:
            new_data_set.append(list(np.array(element)[attributes_chosen])) # By making it a numpy array we can pass lists of indexes as attributes_chosen
            # i.e passing attributes_chosen=[0,2] will do a projection onto the first and third attribute etc
        return new_data_set

    # data_attr: List of indexes telling us what each attribute
    def filter(self, encrypted_data, predicates, CSP, predicate_features=None, data_features=None):#predicate inputed in double binary list i.e. [[0,1,0,1],[1,1,1,0],[1,1]]
        if predicate_features is None:
            predicate_features = range(0, self.num_attr) # If none assume the predicate is over all attributes
        if data_features is None:
            data_features = range(0, self.num_attr) # If none assume the encrypted data has all attributes (i.e has not been projected)

        bit_vector = []
        for row in encrypted_data:
            row_indicator = self.public_key.lab_encrypt(1)
            for i, predicate in enumerate(predicates):
                attribute_indicator = self.public_key.lab_encrypt(0)
                attr_val = row[data_features.index(predicate_features[i])]
                for index in predicate:
                    if index == 1:
                        attribute_indicator._lab_add_encrypted(attr_val[index])
                row_indicator = self.public_key.general_lab_multiplication(row_indicator, attribute_indicator, CSP)
            bit_vector.append(row_indicator)

        return bit_vector
    
    def count(self, bit_vector):
        total = self.public_key.lab_encrypt(0)
        for i, value in enumerate(bit_vector):
            total = value._lab_add_encrypted(total)
        return total

    def group_by_count(self, encrypted_data, attribute, CSP):
        return_vector = []
        new_data_set = self.project(encrypted_data, attribute)
        attribute_size =  len(encrypted_data[0][attribute])
        for value in range(attribute_size):
            predicate = [[0  if i != value else 1 for i in range(attribute_size)]]
            blank, bit_vector = self.filter(new_data_set, predicate, CSP, predicate_features=[attribute]) # predicate_features=[attribute] tells filter to only filter on one attribute (the one provided to GBC)
            return_vector.append(self.count(bit_vector))
        return return_vector
    
    def group_by_count_encoded(self, encrypted_data, attribute, CSP):
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
        gbc_vector = self.group_by_count(encrypted_data, attribute, CSP)
        M = [random.randint(0,10**5) for n in range(len(gbc_vector))]
        gbc_vector_masked = [self.public_key.lab_encrypt(M[i])._lab_add_encrypted(gbc_vector[i]) for i in range(len(gbc_vector))]
        return_vector_encrypted = CSP.group_by_count_encoded(gbc_vector_masked, len(encrypted_data))
        return [rightRotate(return_vector_encrypted[i], M[i]) for i in range(len(return_vector_encrypted))]
                        
