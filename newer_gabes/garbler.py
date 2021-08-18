import copy
import pickle
from newer_gabes.garbledcircuit import GarbledCircuit as Circuit
from cryptography.hazmat.primitives.asymmetric import rsa
from random import randint
from cryptography.hazmat.backends import default_backend
from circuit import circuit

class Alice():
    def __init__(self):
        self.__true_label = None
        self.__false_label = None
        self.__circ = None
        self.__garbler_inputs = None
        self.__d = None
        self.__circ_name = circuit
        self._inputs = {'1': 1, '2': 0}


    def start(self, circ_name = None, inputs = None):
        if circ_name == None:
            circ_name = self.__circ_name
        self.__circ = Circuit(circ_name)
        identifiers = self.hand_over_wire_identifiers()
        if inputs == None:
            self.__garbler_inputs = self._inputs
        else:
            self.__garbler_inputs = inputs
        
        return identifiers


    def hand_over_wire_identifiers(self):
        circ = self.__circ
        identifiers = [wire.identifier for wire in circ.get_input_wires()]
        return identifiers
    
    
    def hand_over_cleaned_circuit(self):
        circ = self.__circ
        new_circ = circ.clean()
        return new_circ
    

    def send_label(self, identifier):
        for item in self.__circ.get_input_wires():
            if identifier == item.identifier:
                wire = item
                break
        if wire.identifier not in self.__garbler_inputs:
            print(wire.identifier)
            print(self.__garbler_inputs)
            raise Exception('identifier doesn\'t appear in garbler or evaluator input lists')
        else:
            chosen_bit = self.__garbler_inputs[wire.identifier]
            if chosen_bit == '1':
                secret_label = wire.true_label
            else:
                secret_label = wire.false_label
            return secret_label

    
    def set_labels(self, identifier):
        for item in self.__circ.get_input_wires():
            if identifier == item.identifier:
                wire = item
                break
        if wire.identifier in self.__garbler_inputs:
            raise Exception('identifier  appears in both garbler or evaluator input lists')
        else:
            self.__false_label = copy.deepcopy(wire.false_label)
            self.__true_label = copy.deepcopy(wire.true_label)
            self.__false_label.represents = self.__true_label.represents = None


    def learn_output(self, output_label):
        circ = self.__circ
        output_gate = circ.tree.name
        out1 = output_gate.output_wire.true_label.to_base64()
        out2 = output_label.to_base64()
        output = out1 == out2
        return output

    
    def garbot1(self):
        private_key = rsa.generate_private_key(public_exponent=65537,key_size=512,backend=default_backend())
        d = private_key.private_numbers().d
        public_key = private_key.public_key()
        m, f = public_key.public_numbers().n, public_key.public_numbers().e
        y0, y1 = [randint(2, m // 2) for _ in range(2)]
        self.__d =  d
        return y0, y1, m, f

        
    def garbot2(self, v, x0, x1, n):
        k0, k1 = [pow((v - x), self.__d, n) for x in (x0, x1)]
        bytes_m0 = pickle.dumps(self.__true_label)
        bytes_m1 = pickle.dumps(self.__false_label)
        m0 = int.from_bytes(bytes_m0, byteorder='big')
        m1 = int.from_bytes(bytes_m1, byteorder='big')
        return m0 + k0, m1 + k1, len(bytes_m0), len(bytes_m1)
