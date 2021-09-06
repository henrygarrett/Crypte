from .PrivacyEngine import PrivacyEngine
from .KeyManager import KeyManager
import numpy as np
import random
import math
from circuits.complete_circuit import Complete_circuit
from garbled_circuits.parties import Alice

class CryptographicServiceProvider():
    def __init__(self, epsilon_budget, generate_keys=False):
        self.privacy_engine = PrivacyEngine(epsilon_budget)
        self.key_manager = KeyManager(generate_keys)
        self.__r = None
        self.alice = None

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

    def noisy_max(self, data, sensitivity, privacy_parameter, k):
        if self.privacy_engine.is_program_allowed(privacy_parameter):
            return [self.key_manager.private_key.lab_decrypt(value) + np.random.default_rng().laplace(scale=(2 * k * sensitivity) / privacy_parameter) for value in data]
        else:
            raise Exception('Privacy Budget Exceeded')
            
    def garbled_circuitnm(self, M, vector_decrypted, k):
        vector_clear = [vector_decrypted[i] - M[i] for i in range(len(vector_decrypted))]
        indices = sorted(range(len(vector_clear)), key=lambda i: vector_clear[i], reverse=True)[:k]
        return indices

    def count_distinct(self, vector_masked):
        how_many = len(vector_masked)
        input_size = 32 # arbitrary. needs to allow for size of input
        base_in = '{:0' + str(input_size) + 'b}'
        base_out = '{:0' + str(math.ceil(math.log(how_many + 0.1, 2))) + 'b}'

        circuit = Complete_circuit(how_many, input_size)
        circuit.subtractor()
        circuit.sieve()
        circuit.adder1()
        circuit.adder2()
        circuit_file = "circuit.json"

        r = random.randint(0, 7)
        a_input = [self.key_manager.private_key.lab_decrypt(i) for i in vector_masked]
        a_input = [int(x) for a in a_input for x in base_in.format(a)]
        add = [int(x) for x in base_out.format(r)]
        add.insert(0, 0)
        a_input = add + a_input

        print(circuit_file)
        self.alice = Alice(a_input, circuit_file)
        self.alice.garble_circuits()  # Garbles circuits, alice stores them
        garbled_circuit = self.alice.garbled_circuits[0]  # only need one circuit
        a_inputs = self.alice.send_inputs
        return {'garbled_circuit': garbled_circuit, 'a_inputs': a_inputs}

    def ot_send(self):
        return self.alice.ot_send()

    def ot_receive(self, w, h0):
        return self.alice.ot_receive(w, h0)