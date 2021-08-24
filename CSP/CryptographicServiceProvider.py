# from pathlib import Path
# path = str(Path.cwd().parents[2])#index needs to be set for cwd which will likely be where operators are run not this file

from .PrivacyEngine import PrivacyEngine
from .KeyManager import KeyManager
import numpy as np
import random

class CryptographicServiceProvider():
    def __init__(self, epsilon_budget, generate_keys=False):
        self.privacy_engine = PrivacyEngine(epsilon_budget)
        self.key_manager = KeyManager(generate_keys)
        self.__r = None

    def __str__(self):
        return "CryptographicServiceProvider" + str(
            {"KeyManager": self.key_manager.__str__(), "PrivacyEngine": self.privacy_engine.__str__()})

    def decrypt_data(self, encrypted_data):
        return [self.decrypt_row(encrypted_row) for encrypted_row in encrypted_data]

    # Should contain an encrypted row of one-hot vectors to be decrypted
    def decrypt_row(self, encrypted_row):
        decrypted_data = []
        for encoded_attr in encrypted_row:
            decrypted_attribute = []
            for encrypted_number in encoded_attr:
                decrypted_attribute.append(self.key_manager.private_key.lab_decrypt(encrypted_number))
            decrypted_data.append(decrypted_attribute)

        return decrypted_data

    def decrypt_bit_vector(self, bit_vector):
        return [self.key_manager.private_key.lab_decrypt(enc) for enc in bit_vector]

    def lab_multiplication(self, intermediary, cipher1, cipher2):
        decrypt_intermediary = self.key_manager.private_key.decrypt(intermediary) + self.key_manager.private_key.decrypt(cipher1.label_encrypted) * self.key_manager.private_key.decrypt(cipher2.label_encrypted)
        return_cipher = self.key_manager.public_key.lab_encrypt(decrypt_intermediary)
        return return_cipher

    def group_by_count_encoded(self, gbc_vector_masked, data_set_size):
        public_key = self.key_manager.public_key
        private_key = self.key_manager.private_key
        gbc_vector_masked_decrypted = [private_key.lab_decrypt(value) for value in gbc_vector_masked]
        return_vector = []
        for i, value in enumerate(gbc_vector_masked_decrypted):
            return_vector.append([])
            for j in range(data_set_size + 1):
                if j != (value % (data_set_size + 1)):
                    return_vector[i].append(0)
                else:
                    return_vector[i].append(1)
        return_vector_encrypted = [[public_key.lab_encrypt(bit) for bit in value] for value in return_vector]
        return return_vector_encrypted
    
    def count_distinct(self, vector_masked):
        vector_decrypted = [self.key_manager.private_key.lab_decrypt(i) for i in vector_masked]
        return vector_decrypted
    def random_r(self):
        r = random.randint(0,10**40)
        self.__r = r
        return self.key_manager.public_key.lab_encrypt(r)
    def garbled_circuitcd(self, M, vector_decrypted):
        r = self.__r
        vector_clear = [vector_decrypted[i] - M[i] for i in range(len(M))]
        count_masked = np.count_nonzero(vector_clear) + r
        return count_masked
    
    
    def laplace(self, data, sensitivity, privacy_parameter):
        if self.privacy_engine.is_program_allowed(privacy_parameter):
            return [self.key_manager.private_key.lab_decrypt(value) + np.random.default_rng().laplace(scale=(2*sensitivity)/privacy_parameter) for value in data]
        else:
            raise Exception('Privacy Budget Exceeded')


    def noisy_max(self, data, sensitivity, privacy_parameter, how_many, CSP):
        if self.privacy_engine.is_program_allowed(privacy_parameter):
            return [self.key_manager.private_key.lab_decrypt(value) + np.random.default_rng().laplace(scale=(2*how_many*sensitivity)/privacy_parameter) for value in data]
        else:
            raise Exception('Privacy Budget Exceeded')
            
    def garbled_circuitnm(self, M, vector_decrypted, how_many):
        vector_clear = [vector_decrypted[i] - M[i] for i in range(len(vector_decrypted))]
        indices = sorted(range(len(vector_clear)), key=lambda i: vector_clear[i])[-how_many:]
        return indices