import math
import random
import numpy as np
import copy

class ProgramExecutor():
    def __init__(self, public_key, num_rows, num_attr):
        self.public_key = public_key
        self.num_rows = num_rows # Number of rows in the dataset
        self.num_attr = num_attr # Number of attributes in the dataset
        self.sensitivity = 1
        # Both of the above are needed for filtering

    def reset_sensitivity(self):
        self.sensitivity = 1
    
    def cross_product(self, encrypted_data, attribute1, attribute2, CSP):
        new_data_set = copy.deepcopy(encrypted_data)
        for i, element in enumerate(new_data_set):
            vector1 = element.pop(attribute1)
            vector2 = element.pop(attribute2 if attribute1 > attribute2 else attribute2 - 1)
            vector_new = []
            for i in range(len(vector1)*len(vector2)):
                vector_new.append(self.public_key.general_lab_multiplication(vector1[math.floor(i/len(vector2))], vector2[i%len(vector2)], CSP))
            element.append(vector_new)
        return new_data_set

    def project(self, encrypted_data, attributes_chosen):
        attributes_chosen = [attributes_chosen] if type(attributes_chosen) == int else attributes_chosen
        new_data_set = []
        for row in encrypted_data:
            new_data_set.append(list(np.array(row, dtype="object", ndmin=1)[attributes_chosen])) # By making it a numpy array we can pass lists of indexes as attributes_chosen
            # i.e passing attributes_chosen=[0,2] will do a projection onto the first and third attribute etc
        return new_data_set

    # data_attr: List of indexes telling us what each attribute
    def filter(self, encrypted_data, predicates, CSP, predicate_features=None, data_features=None):#predicate inputed in double binary list i.e. [[0,1,0,1],[1,1,1,0],[1,1]]
        # TODO: Error check to ensure predicate_features subset of data_features
        if predicate_features is None:
            predicate_features = range(0, self.num_attr) # If none assume the predicate is over all attributes
        if data_features is None:
            data_features = range(0, self.num_attr) # If none assume the encrypted data has all attributes (i.e has not been projected)

        bit_vector = []
        enc_one = self.public_key.lab_encrypt(1)
        enc_zero = self.public_key.lab_encrypt(0)

        for i, row in enumerate(encrypted_data):
            row_indicator = copy.deepcopy(enc_one)
            for j, predicate in enumerate(predicates):
                attribute_indicator = copy.deepcopy(enc_zero)
                attr_val = row[data_features.index(predicate_features[j])]
                for k,index in enumerate(predicate):
                    if index == 1:
                        attribute_indicator = attribute_indicator._lab_add_encrypted(attr_val[k])
                row_indicator = self.public_key.general_lab_multiplication(row_indicator, attribute_indicator, CSP)

            bit_vector.append(row_indicator)

        return bit_vector
    
    def count(self, bit_vector):
        total = self.public_key.lab_encrypt(0)
        for i, value in enumerate(bit_vector):
            total = value._lab_add_encrypted(total)
        return total

    def group_by_count(self, encrypted_data, attribute, CSP):
        self.sensitivity *= 2
        return_vector = []
        new_data_set = self.project(encrypted_data, attribute)
        attribute_size =  len(encrypted_data[0][attribute])
        for value in range(attribute_size):
            predicate = [[0  if i != value else 1 for i in range(attribute_size)]]
            bit_vector = self.filter(new_data_set, predicate, CSP, predicate_features=[attribute], data_features=[attribute]) # predicate_features=[attribute] tells filter to only filter on one attribute (the one provided to GBC)
            return_vector.append(self.count(bit_vector))
        return return_vector
    
    def group_by_count_encoded(self, encrypted_data, attribute, CSP):
        self.sensitivity *= 2
        def rightRotate(lists, num):
            output_list = []
            length = len(lists)
            # Will add values from n up to the new list
            for item in range(num % length, length):
                output_list.append(lists[item])
              
            # Will add the values before n to the end of new list    
            for item in range(0, num % length): 
                output_list.append(lists[item])

            return output_list
        gbc_vector = self.group_by_count(encrypted_data, attribute, CSP)
        M = [random.randint(0,10**5) for n in range(len(gbc_vector))]
        gbc_vector_masked = [self.public_key.lab_encrypt(M[i])._lab_add_encrypted(gbc_vector[i]) for i in range(len(gbc_vector))]
        return_vector_encrypted = CSP.group_by_count_encoded(gbc_vector_masked, len(encrypted_data))
        return [rightRotate(item, M[i]) for i, item in enumerate(return_vector_encrypted)]
    
    def count_distinct(self, input_vector, CSP):
        M = [random.randint(0,10**10) for _ in range(len(input_vector))]
        vector_masked = [input_vector[i]._lab_add_encrypted(self.public_key.lab_encrypt(M[i])) for i in range(len(M))]
        vector_decrypted = CSP.count_distinct(vector_masked)
        r_enc = CSP.random_r()
        count_masked = CSP.garbled_circuitcd(M, vector_decrypted)
        count_encrypted = self.public_key.lab_encrypt(count_masked)._lab_subtract_encrypted(r_enc)
        return count_encrypted

    def laplace(self, data, privacy_parameter, CSP):
        data = data if type(data) == list else [data]
        noisy_data = [value._lab_add_encrypted(self.public_key.lab_encrypt(np.random.default_rng().laplace(scale=(2*self.sensitivity)/privacy_parameter))) for value in data]
        return CSP.laplace(noisy_data, self.sensitivity, privacy_parameter)
    
    def noisy_max(self, data, privacy_parameter, CSP, k):
         M = [random.randint(0,10**10) for _ in range(len(data))]
         M_enc = [self.public_key.lab_encrypt(m) for m in M]
         noise = [self.public_key.lab_encrypt(np.random.default_rng().laplace(scale=(2 * k * self.sensitivity) / privacy_parameter)) for _ in range(len(data))]
         noisy_data = [data[i]._lab_add_encrypted(noise[i])._lab_add_encrypted(M_enc[i]) for i in range(len(data))]
         data_decrypted = CSP.noisy_max(noisy_data, self.sensitivity, privacy_parameter, k)
         return CSP.garbled_circuitnm(M, data_decrypted, k)